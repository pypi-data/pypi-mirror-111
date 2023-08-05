"""
Utilities for parsing CSV files.
"""

from ..utils.py3 import textstring

from ..utils import string, funcargparse

import re
import numpy as np
import pandas as pd


_table_delimiters=string._delimiters
_table_delimiters_regexp=re.compile(_table_delimiters)

def _read_table_raw(f, delimiters=_table_delimiters_regexp, empty_entry_substitute=None, stop_comment=None, chunk_size=None, as_text=True, simple_entries=True):
    r"""
    Load data table (in text format) and comments from the opened file `f` (must be open as binary).
    
    Comment lines are the ones starting with ``#``.
    
    Args:
        delimiters (str): Regex string which recognizes delimiters (by default ``r"\s*,\s*|\s+"``, i.e., commas and whitespaces).
        empty_entry_substitute: Substitute for empty table entries. If ``None``, all empty table entries are skipped.
        stop_comment (str): Regex string for the stopping comment.
            If not ``None``. the function will stop if comment satisfying `stop_comment` regex is encountered.
        chunk_size (int): Maximal size (number of lines) of the data to read.
        as_text (bool): If ``False``, return entries as strings; otherwise, convert them into values.
        simple_entries (bool): If ``True``, assume that there are no escaped strings or parenthesis structures in the files,
            so line splitting routine is simplified.
            
    Returns:
        tuple: ``(data, comments, finished)``, where data is 2D-list of table entries (already recognized unless ``as_text==True``)
            and `comments` is a list of strings. Data lines may have different lengths.
            `finished` indicates if file has been read through the end (it's ``True`` unless `chunk_size` is not ``None``).
    """
    delimiters=re.compile(delimiters)
    data=[]
    comment_lines=[]
    line=f.readline()
    cnt=0
    while line:
        line=line.strip()
        if line:
            if line[:1]!='#': # data row
                if simple_entries:
                    line=delimiters.split(line)
                    if not as_text:
                        line=[string.from_string(e) for e in line]
                    empty_string=""
                else:
                    line=string.from_row_string(line,delimiters,return_string=as_text)
                empty_string="" if (simple_entries or as_text) else string.empty_string
                if empty_entry_substitute is None:
                    line=[el for el in line if el is not empty_string]
                else:
                    line=[(el if el!=empty_string else empty_entry_substitute) for el in line]
                data.append(line)
            else:
                if stop_comment is not None and re.match(stop_comment,line[1:]) is not None: #end of continuous block
                    break
                else:
                    comment_lines.append(line.lstrip("# \t"))
        cnt=cnt+1
        if chunk_size is not None and cnt==chunk_size:
            return data,comment_lines,False
        line=f.readline()
    return data,comment_lines,True




def _try_convert_element(element, dtype="numeric"):
    # if dtype=="complex":
    #     return [complex(e.lower().replace('i','j')) for e in line]
    # else:
    if dtype=="raw":
        return element
    if dtype=="generic":
        return string.from_string(element)
    elif dtype=="numeric":
        element=string.from_string(element)
        try:
            complex(element)
            return element
        except (TypeError, ValueError):
            raise ValueError("malformed element")
    else:
        return np.asscalar(np.array(element).astype(dtype))
def _try_convert_row(line, dtype):
    """
    Try and parse a single line with a given dtype.
    """
    dtype=funcargparse.as_sequence(dtype,len(line),allowed_type="builtin;nostring",length_conflict_action="error")
    return np.array([_try_convert_element(e,dt) for e,dt in zip(line,dtype)])
def _get_row_length(table, dtype):
    if funcargparse.is_sequence(dtype,"builtin;nostring"):
        row_len=len(dtype)
    else:
        row_len=None
        for row in table:
            try:
                row_len=len(_try_convert_row(row,dtype))
                break
            except ValueError:
                pass
        return row_len
def _try_convert_column(column, dtype, min_dtype="int"):
    """
    Try and parse a single column with a given dtype.
    Return tuple converted_column, actual_dtype.
    If dtype=="generic" or dtype=="numeric", min_dtype determines "minimal" (in a sense that int<float<complex<generic) dtype.
        If min_dtype!="generic", the routine first tries to convert the whole column into a numpy array, gradually increasing types on fails. 
    """
    if len(column)>0 and not isinstance(column[0],textstring):
        raise ValueError("_try_convert_column only works for string input")
    if dtype=="raw":
        return column, dtype
    elif dtype in {"numeric","generic"}:
        if min_dtype!="generic":
            dtypes_order=["int","float","complex"]
            start_dtype=dtypes_order.index(min_dtype)
            column_array=np.array(column)
            for dt in dtypes_order[start_dtype:]:
                try:
                    return column_array.astype(dt), dt
                except ValueError:
                    pass
                except OverflowError: # need to use the standard Python long integer type, which can't be stored in a numpy array 
                    break
                except TypeError: # some numpy version can not convert string into complex
                    break
        column=[string.from_string(e) for e in column]
        if dtype=="numeric":
            for e in column:
                complex(e) # check numeric nature
        min_dtype="generic" if dtype=="numeric" else dtype
        return column, min_dtype
    else:
        if np.dtype(dtype).kind=="c":
            column=[complex(e) for e in column] # numpy converts text into int/float, but not into complex, so it needs to be converted manually
        return np.array(column,dtype=dtype), dtype # dtype is specified, just convert
def _make_empty_column(dtype):
    if dtype=="numeric":
        return _try_convert_column([],dtype)[0]
    else:
        return _try_convert_column([],dtype,min_dtype=dtype)[0]

class ChunksAccumulator:
    """
    Class for accumulating data chunks into a single array.
    
    Args:
        dtype: dtype of entries; can be either a single type, or a list of types (one per column).
            Possible dtypes are: ``'int'``, ``'float'``, ``'complex'``,
            ``'numeric'`` (tries to coerce to minimal possible numeric type, raises error if data can't be converted to complex),
            ``'generic'`` (accept arbitrary types, including lists, dictionaries, escaped strings, etc.), ``'raw'`` (keep raw string).
        ignore_corrupted_lines: if ``True``, skip corrupted (e.g., non-numeric for numeric dtype, or with too few entries) lines;
            otherwise, raise :exc:`ValueError`.
        trim_rows: if ``True`` and the row length is larger than expected, drop extra entries; otherwise, treat the row as corrupted
    """
    def __init__(self, dtype="numeric", ignore_corrupted_lines=True, trim_rows=False):
        self.dtype=dtype
        self.row_size=len(dtype) if funcargparse.is_sequence(dtype,"builtin;nostring") else None
        self.min_dtype=None if self.row_size is None else ["int"]*self.row_size
        self.ignore_corrupted_lines=ignore_corrupted_lines
        self.trim_rows=trim_rows
        self.corrupted_lines={"size":[],"type":[]}
        self.columns=[]
    def corrupted_number(self):
        return len(self.corrupted_lines["size"])+len(self.corrupted_lines["type"])
    def convert_columns(self, raw_columns):
        """
        Convert raw columns into appropriate data structure (numpy array for numeric dtypes, list for generic and raw).
        """
        columns=[]
        new_min_dtype=[]
        for rc,dt,mdt in zip(raw_columns,self.dtype,self.min_dtype):
            c,mdt=_try_convert_column(rc,dt,mdt)
            new_min_dtype.append(mdt)
            columns.append(c)
        self.min_dtype=new_min_dtype
        return columns
    def add_columns(self, columns):
        """
        Append columns (lists or numpy arrays) to the existing data.
        """
        if columns==[]:
            return
        if self.columns==[]:
            self.columns=columns
        else:
            new_columns=[]
            for c,ac in zip(self.columns,columns):
                if isinstance(c,np.ndarray) and isinstance(ac,np.ndarray):
                    nc=np.concatenate((c,ac))
                elif isinstance(ac,np.ndarray):
                    nc=c+list(ac)
                elif isinstance(c,np.ndarray):
                    nc=list(c)+ac
                else:
                    nc=c+ac
                new_columns.append(nc)
            self.columns=new_columns
    def add_chunk(self, chunk):
        """
        Add a chunk (2D list) to the pre-existing data.
        """
        # determine row size
        if self.row_size is None:
            self.row_size=_get_row_length(chunk,self.dtype)
            if self.row_size is None:
                self.corrupted_lines["type"]=self.corrupted_lines["type"]+chunk
                return
            else:
                self.min_dtype=["int"]*self.row_size
                self.dtype=[self.dtype]*self.row_size
        row_size=self.row_size
        # trim chunks
        trimmed_chunk=[]
        for row in chunk:
            if len(row)==row_size or (len(row)>row_size and self.trim_rows):
                trimmed_chunk.append(row[:row_size])
            else:
                if self.ignore_corrupted_lines:
                    self.corrupted_lines["size"].append(row)
                else:
                    raise ValueError("size of the row doesn't agree with the number of columns")
        # convert chunks
        try:
            raw_columns=zip(*trimmed_chunk)
            columns=self.convert_columns(raw_columns)
        except ValueError:
            filtered_chunk=[]
            dtype=self.dtype
            for row in trimmed_chunk:
                try:
                    #filtered_chunk.append([_try_convert_element(e,dt) for e,dt in zip(row,dtype)])
                    # check convertibility, but otherwise leave in raw state
                    for e,dt in zip(row,dtype):
                        _try_convert_element(e,dt)
                    filtered_chunk.append(row)
                except ValueError:
                    self.corrupted_lines["type"].append(row)
            raw_columns=zip(*filtered_chunk)
            columns=self.convert_columns(raw_columns)
        self.add_columns(columns)


_complex_dtypes={"generic","raw"} # dtypes for which simple_entries==False (they can potentially be strings or lists, so that splitting lines is more complicated)
def read_columns(f, dtype, delimiters=_table_delimiters, empty_entry_substitute=None, ignore_corrupted_lines=True, trim_rows=False, stop_comment=None):
    r"""
    Load columns from the file stream `f`.
    
    Args:
        dtype: dtype of entries; can be either a single type, or a list of types (one per column).
            Possible dtypes are: ``'int'``, ``'float'``, ``'complex'``,
            ``'numeric'`` (tries to coerce to minimal possible numeric type, raises error if data can't be converted to complex),
            ``'generic'`` (accept arbitrary types, including lists, dictionaries, escaped strings, etc.), ``'raw'`` (keep raw string).
        delimiters (str): Regex string which recognizes delimiters (by default ``r"\s*,\s*|\s+"``, i.e., commas and whitespaces).
        empty_entry_substitute: Substitute for empty table entries. If ``None``, all empty table entries are skipped.
        ignore_corrupted_lines: If ``True``, skip corrupted (e.g., non-numeric for numeric dtype, or with too few entries) lines;
            otherwise, raise :exc:`ValueError`.
        trim_rows: if ``True`` and the row length is larger than expected, drop extra entries; otherwise, treat the row as corrupted
        stop_comment (str): Regex string for the stopping comment.
            If not ``None``. the function will stop if comment satisfying `stop_comment` regex is encountered.
            
    Returns:
        tuple: ``(columns, comments, corrupted_lines)``.
        
            `columns` is a list of columns with data.
            
            `comments` is a list of comment strings.
            
            `corrupted_lines` is a dict ``{'size':list, 'type':list}`` of corrupted lines (already split into entries),
            based on the corruption type (``'size'`` means too small size, ``'type'`` means it couldn't be converted using provided dtype).
    """
    original_chunk_size=1000
    chunk_multiplier=1.5
    chunk_size=original_chunk_size
    comments=[]
    accum=ChunksAccumulator(dtype,ignore_corrupted_lines=ignore_corrupted_lines,trim_rows=trim_rows)
    if funcargparse.is_sequence(dtype,"builtin;nostring"):
        generic_dtype=any(dt in _complex_dtypes for dt in dtype)
    else:
        generic_dtype=dtype in _complex_dtypes
    finished=False
    while not finished:
        current_corrupted=accum.corrupted_number()
        chunk,chunk_comments,chunk_finished=_read_table_raw(f,
                        delimiters=delimiters,empty_entry_substitute=empty_entry_substitute,stop_comment=stop_comment,chunk_size=chunk_size,simple_entries=not generic_dtype)
        finished=finished or chunk_finished
        comments=comments+chunk_comments
        accum.add_chunk(chunk)
        if accum.corrupted_number()==current_corrupted:
            chunk_size=int(chunk_size*chunk_multiplier)
        else:
            chunk_size=max(int(chunk_size/chunk_multiplier),original_chunk_size)
    return accum.columns,comments,accum.corrupted_lines

def _get_columns_number(data=None, columns=None, dtype=None):
    ldata=len(data) if data else None
    if funcargparse.is_sequence(columns,"builtin;nostring"):
        lcolumns=len(columns)
    else:
        lcolumns=columns
    ldtype=len(dtype) if funcargparse.is_sequence(dtype,"builtin;nostring") else None
    lens={k:l for (k,l) in [("data",ldata),("columns",lcolumns),("dtype",ldtype)] if l is not None}
    if not lens:
        return None
    elif len(lens)>1:
        for k1 in lens:
            for k2 in lens:
                if lens[k1]!=lens[k2]:
                    raise ValueError("{} length {} doesn't agree with {} length {}".format(k1,lens[k1],k2,lens[k2]))
    return lens.popitem()[1]
    

def columns_to_table(data, columns=None, dtype="numeric", out_type="columns"):
    """
    Convert `data` (columns list) into a table.
    
    Args:
        columns: either number if columns, or a list of columns names.
        out_type (str): type of the result: ``'array'`` for numpy array, ``'pandas'`` for pandas DataFrame, ``'columns'`` for tuple ``(data, columns)``
    """
    funcargparse.check_parameter_range(out_type,"out_type",{"array","pandas","columns"})
    col_num=_get_columns_number(data,columns,dtype)
    if col_num:
        columns=columns if funcargparse.is_sequence(columns,"builtin;nostring") else list(range(col_num))
        dtype=funcargparse.as_sequence(dtype,col_num,allowed_type="builtin;nostring")
        if not data:
            data=[_make_empty_column(dt) for dt in dtype]
    else:
        data=[]
    if out_type=="array":
        if col_num:
            return np.column_stack(data)
        else:
            return _make_empty_column(dtype)
    elif out_type=="pandas":
        if col_num:
            return pd.DataFrame(dict(zip(columns,data)),columns=columns)
        else:
            return pd.DataFrame()
    else:
        if col_num:
            return data,columns
        else:
            return [],[]


def read_table(f, dtype="numeric", columns=None, out_type="columns", delimiters=_table_delimiters, empty_entry_substitute=None, ignore_corrupted_lines=True, trim_rows=False, stop_comment=None):
    """
    Load table from the file stream `f`.
    
    Arguments are the same as in :func:`read_columns` and :func:`columns_to_table`.
    
    Returns:
        tuple: ``(table, comments, corrupted_lines)``.
        
            `table` is a table of the format `out_type`.
            
            `corrupted_lines` is a dict ``{'size':list, 'type':list}`` of corrupted lines (already split into entries),
            based on the corruption type (``'size'`` means too small size, ``'type'`` means it couldn't be converted using provided dtype).
            
            `comments` is a list of comment strings.
    """
    col_num=_get_columns_number(columns=columns,dtype=dtype)
    if col_num is not None:
        dtype=funcargparse.as_sequence(dtype,col_num,allowed_type="builtin;nostring")
    data,comments,corrupted_lines=read_columns(f,dtype,
                    delimiters=delimiters,empty_entry_substitute=empty_entry_substitute,stop_comment=stop_comment,ignore_corrupted_lines=ignore_corrupted_lines,trim_rows=trim_rows)
    return columns_to_table(data,columns=columns,dtype=dtype,out_type=out_type),comments,corrupted_lines