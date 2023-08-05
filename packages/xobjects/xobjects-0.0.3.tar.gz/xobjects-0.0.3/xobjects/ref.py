import logging

import numpy as np

from .typeutils import Info, dispatch_arg, get_a_buffer
from .scalar import Int64
from .array import Array
from . import capi

log = logging.getLogger(__name__)

NULLVALUE = -(2 ** 63)
NULLTYPE = -1
NULLREF = np.array([NULLVALUE, NULLTYPE], dtype="int64")


class MetaRef(type):
    def __getitem__(cls, rtypes):
        if not isinstance(rtypes, tuple):
            rtypes = (rtypes,)
        return cls(*rtypes)


class Ref(metaclass=MetaRef):
    def __init__(self, *rtypes):
        self._rtypes = rtypes
        # self._rtypes_names = [tt.__name__ for tt in rtypes]
        self.__name__ = "Ref" + "".join(tt.__name__ for tt in self._rtypes)
        self._c_type = self.__name__

        if len(rtypes) == 1:
            self._is_union = False
            self._size = 8
        else:
            self._is_union = True
            self._size = 16

    def _typeid_from_type(self, typ):
        for ii, tt in enumerate(self._rtypes):
            if tt.__name__ == typ.__name__:
                return ii
        # If no match found:
        raise TypeError(f"{typ} is not memberof {self}!")

    def _typeid_from_name(self, name):
        for ii, tt in enumerate(self._rtypes):
            if tt.__name__ == name:
                return ii
        # If no match found:
        raise TypeError(f"{name} is not memberof {self}")

    def _type_from_typeid(self, typeid):
        for ii, tt in enumerate(self._rtypes):
            if ii == typeid:
                return tt
        # If no match found:
        raise TypeError(f"Invalid id: {typeid}!")

    def _is_member(self, rtype):
        for tt in self._rtypes:
            if rtype.__name__ == tt.__name__:
                return True
        return False

    def _type_from_name(self, name):
        for tt in self._rtypes:
            if tt.__name__ == name:
                return tt
        # If no match found:
        raise TypeError(f"Invalid name: {name}!")

    def _get_stored_type(self, buffer, offset):
        typeid = Int64._from_buffer(buffer, offset + 8)
        return self._type_from_typeid(typeid)

    def _from_buffer(self, buffer, offset):
        refoffset = Int64._from_buffer(buffer, offset)
        if refoffset == NULLVALUE:
            return None
        else:
            refoffset += offset
            if self._is_union:
                rtype = self._get_stored_type(buffer, refoffset)
            else:
                rtype = self._rtypes[0]
            return rtype._from_buffer(buffer, refoffset)

    def _to_buffer(self, buffer, offset, value, info=None):

        # Get/set reference type
        if self._is_union:
            if value is None:
                # Use the first type (default)
                rtype = -1  # self._rtypes[0]
                Int64._to_buffer(buffer, offset + 8, -1)
            elif self._is_member(value.__class__):
                rtype = value.__class__
                typeid = self._typeid_from_type(rtype)
                Int64._to_buffer(buffer, offset + 8, typeid)
            elif isinstance(value, tuple):
                rtype = self._typeid_from_name(value[0])
                Int64._to_buffer(buffer, offset + 8, typeid)
            else:
                # Keep old type
                rtype = self._get_stored_type(buffer, offset)
        else:
            rtype = self._rtypes[0]

        # Get/set content
        if value is None:
            refoffset = NULLVALUE  # NULL value
            Int64._to_buffer(buffer, offset, refoffset)
        elif (
            value.__class__.__name__ == rtype.__name__  # same type
            and value._buffer is buffer
        ):
            refoffset = value._offset - offset
            Int64._to_buffer(buffer, offset, refoffset)

        else:
            newobj = rtype(value, _buffer=buffer)
            refoffset = newobj._offset - offset
            Int64._to_buffer(buffer, offset, refoffset)

    def __call__(self, *args):
        if len(args) == 0:
            return None
        else:
            if self._is_union:
                name, value = args
                return self._type_from_name(name)(value)
            else:
                (value,) = args
                return self._rtypes[0](value)

    def _inspect_args(self, arg):
        return Info(size=self._size)

    def __getitem__(self, shape):
        return Array.mk_arrayclass(self, shape)

    def _get_c_offset(self, conf):
        itype = conf.get("itype", "int64_t")
        doffset = f"offset"  # starts of data
        return [f"  offset=(({itype}*) obj)[{doffset}];"]

    def _gen_data_paths(self, base=None):
        paths = []
        if base is None:
            base = []
        if self._is_union:
            paths.append(base + [self])
            for rtype in self._rtypes:
                if hasattr(rtype, "_gen_data_paths"):
                    paths.extend(rtype._gen_data_paths())
        else:
            rtype = self._rtypes[0]
            if hasattr(rtype, "_gen_data_paths"):
                paths.extend(rtype._gen_data_paths(base + [self]))
        return paths

    def _gen_c_api(self, conf={}):
        paths = self._gen_data_paths()
        return capi.gen_code(paths, conf)

    def __repr__(self):
        return f"<ref {self.__name__}>"


class MetaUnionRef(type):
    _reftypes: list

    def __new__(cls, name, bases, data):
        if "_c_type" not in data:
            data["_c_type"] = name

        return type.__new__(cls, name, bases, data)

    def _is_member(cls, value):
        typ = value.__class__
        for tt in cls._reftypes:
            if tt.__name__ == typ.__name__:
                return True
        return False

    def _typeid_from_type(cls, typ):
        for ii, tt in enumerate(cls._reftypes):
            if tt.__name__ == typ.__name__:
                return ii
        # If no match found:
        raise TypeError(f"{typ} is not memberof {cls}!")

    def _typeid_from_name(cls, name):
        for ii, tt in enumerate(cls._reftypes):
            if tt.__name__ == name:
                return ii
        # If no match found:
        raise TypeError(f"{name} is not memberof {cls}")

    def _type_from_name(cls, name):
        for tt in cls._reftypes:
            if tt.__name__ == name:
                return tt
        # If no match found:
        raise TypeError(f"{name} is not memberof {cls}")

    def _type_from_typeid(cls, typeid):
        for ii, tt in enumerate(cls._reftypes):
            if ii == typeid:
                return tt
        # If no match found:
        raise TypeError(f"Invalid id: {typeid}!")

    def _from_buffer(cls, buffer, offset):
        refoffset, typeid = Int64._array_from_buffer(buffer, offset, 2)
        if refoffset == NULLVALUE:
            return None
        else:
            rtype = cls._type_from_typeid(typeid)
            return rtype._from_buffer(buffer, offset + refoffset)

    def _inspect_args(cls, *args):
        """
        A unionref can be initialized with an instance of the classes in reftypes or
        a tuple (typename, dictionary)

        Input:
        - None
        - XObject
        - typename, dict
        """
        log.debug(f"get info for {cls} from {args}")
        info = Info(size=cls._size)
        return info

    def _to_buffer(cls, buffer, offset, value, info=None):
        if isinstance(value, cls):  # binary copy
            buffer.update_from_xbuffer(
                offset, value._buffer, value._offset, value._size
            )
        else:
            if value is None:
                xobj = None
            elif isinstance(value, tuple):
                if len(value) == 0:
                    xobj = None
                    typeid = None
                elif len(value) == 1:  # must be XObject or None
                    xobj = value[0]
                    if xobj is not None:
                        typ = xobj.__class__
                        typeid = cls._typeid_from_type(typ)
                        if xobj._buffer != buffer:
                            xobj = typ(xobj, _buffer=buffer)
                elif len(value) == 2:  # must be (str,dict)
                    tname, data = value
                    typ = cls._type_from_name(tname)
                    typeid = cls._typeid_from_name(tname)
                    xobj = typ(data, _buffer=buffer)
            elif cls._is_member(value):
                xobj = value
                typ = xobj.__class__
                typeid = cls._typeid_from_type(typ)
                if xobj._buffer != buffer:
                    xobj = typ(xobj, _buffer=buffer)
            else:
                raise ValueError(f"{value} not handled")
            if xobj is None:
                Int64._array_to_buffer(buffer, offset, NULLREF)
            else:
                ref = np.array([xobj._offset - offset, typeid])
                Int64._array_to_buffer(buffer, offset, ref)

    def __getitem__(cls, shape):
        return Array.mk_arrayclass(cls, shape)

    def _pre_init(cls, *arg, **kwargs):
        return kwargs


class UnionRef(metaclass=MetaUnionRef):
    _size = 16

    def __init__(
        self, *args, _context=None, _buffer=None, _offset=None, **kwargs
    ):
        cls = self.__class__

        args, _ = self._pre_init(*args, **kwargs)

        self._buffer, self._offset = get_a_buffer(
            cls._size, _context, _buffer, _offset
        )

        cls._to_buffer(self._buffer, self._offset, args)

        self._post_init()

    def get(self):
        reloffset, typeid = Int64._array_from_buffer(
            self._buffer, self._offset, 2
        )
        if reloffset == NULLVALUE:
            return None
        else:
            cls = self.__class__
            typ = cls._type_from_typeid(typeid)
            offset = self._offset + reloffset
            return typ._from_buffer(self._buffer, offset)

    @classmethod
    def _pre_init(cls, *args, **kwargs):
        return args, kwargs

    def _post_init(self):
        pass

    @classmethod
    def _gen_data_paths(cls, base=None):
        paths = []
        if base is None:
            base = []
        paths.append(base + [cls])
        for rtype in cls._reftypes:
            if hasattr(rtype, "_gen_data_paths"):
                paths.extend(rtype._gen_data_paths())
        return paths

    @classmethod
    def _gen_c_api(cls, conf={}):
        paths = cls._gen_data_paths()
        return capi.gen_code(paths, conf)
