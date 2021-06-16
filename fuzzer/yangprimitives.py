import boofuzz
import random
import libyang
import string
import exrex

class Int(boofuzz.Fuzzable):
    def __init__(
            self,
            name=None,
            default_value=None,
            min_val=0,
            max_val=1,
            max_mutations=1000,
            seed=None,
            *args,
            **kwargs
    ):
        self.min_val = min_val
        self.max_val = max_val
        self.max_mutations = max_mutations
        self.seed = seed
        self.default_value = default_value
        if default_value is None:
            self.default_value = random.randint(self.min_val, self.max_val)

        super(Int, self).__init__(name=name, default_value=str(self.default_value), *args, **kwargs)


    def mutations(self, default_value):
        last_val = None
        if self.seed is not None:
            random.seed(self.seed)
        
        for i in range(self.max_mutations):
            if i == 0:
                current_val = default_value
            else:
                current_val = random.randint(self.min_val, self.max_val)

            current_val = str(current_val)

            if last_val == current_val:
                continue

            last_val = current_val
            yield current_val

    def encode (self, value, mutation_context=None):
        return value.encode()

class Int8(Int):
    int8_max = 2 ** 7 - 1
    int8_min = -2 ** 7

    def __init__(
            self,
            name=None,
            default_value=None,
            min_val=int8_min,
            max_val=int8_max,
            max_mutations=1000,
            seed=None,
            *args,
            **kwargs
    ):
        if min_val == "min":
            min_val = Int8.int8_min
        else:
            min_val = int(min_val)

        if max_val == "max":
            max_val = Int8.int8_max
        else:
            max_val = int(max_val)

        if min_val < Int8.int8_min:
            raise ValueError("min value too low for int8 type")

        if max_val > Int8.int8_max:
            raise ValueError("max value too big for int8 type")

        super(Int8, self).__init__(name=name, default_value=default_value, min_val=min_val, max_val=max_val,
                max_mutations=max_mutations, seed=seed, *args, **kwargs)

class Int16(Int):
    int16_max = 2 ** 15 -1
    int16_min = -2 ** 15

    def __init__(
            self,
            name=None,
            default_value=None,
            min_val=int16_min,
            max_val=int16_max,
            max_mutations=1000,
            seed=None,
            *args,
            **kwargs
    ):
        if min_val == "min":
            min_val = Int16.int16_min
        else:
            min_val = int(min_val)

        if max_val == "max":
            max_val = Int16.int16_max
        else:
            max_val = int(max_val)

        if min_val < Int16.int16_min:
            raise ValueError("min value too low for int16 type")

        if max_val > Int16.int16_max:
            raise ValueError("max value too big for int16 type")

        super(Int16, self).__init__(name=name, default_value=default_value, min_val=min_val, max_val=max_val,
                max_mutations=max_mutations, seed=seed, *args, **kwargs)

class Int32(Int):
    int32_max = 2 ** 31 -1
    int32_min = -2 ** 31

    def __init__(
            self,
            name=None,
            default_value=None,
            min_val=int32_min,
            max_val=int32_max,
            max_mutations=1000,
            seed=None,
            *args,
            **kwargs
    ):
        if min_val == "min":
            min_val = Int32.int32_min
        else:
            min_val = int(min_val)

        if max_val == "max":
            max_val = Int32.int32_max
        else:
            max_val = int(max_val)

        if min_val < Int32.int32_min:
            raise ValueError("min value too low for int32 type")

        if max_val > Int32.int32_max:
            raise ValueError("max value too big for int32 type")

        super(Int32, self).__init__(name=name, default_value=default_value, min_val=min_val, max_val=max_val,
                max_mutations=max_mutations, seed=seed, *args, **kwargs)

class Int64(Int):
    int64_max = 2 ** 63 -1
    int64_min = -2 ** 63

    def __init__(
            self,
            name=None,
            default_value=None,
            min_val=int64_min,
            max_val=int64_max,
            max_mutations=1000,
            seed=None,
            *args,
            **kwargs
    ):
        if min_val == "min":
            min_val = Int64.int64_min
        else:
            min_val = int(min_val)

        if max_val == "max":
            max_val = Int64.int64_max
        else:
            max_val = int(max_val)

        if min_val < Int64.int64_min:
            raise ValueError("min value too low for int64 type")

        if max_val > Int64.int64_max:
            raise ValueError("max value too big for int64 type")

        super(Int64, self).__init__(name=name, default_value=default_value, min_val=min_val, max_val=max_val,
                max_mutations=max_mutations, seed=seed, *args, **kwargs)

class String(boofuzz.Fuzzable):
    def __init__(
            self,
            name=None,
            default_value=None,
            min_val=10,
            max_val=256,
            patterns=None,
            max_mutations=1,
            seed=None,
            *args,
            **kwargs
    ):
        self.min_val = int(min_val)
        self.max_val = int(max_val)
        self.max_mutations = max_mutations
        self.seed = seed

        self.default_value = default_value
        if default_value is None:
            if patterns:
                print(patterns[0])
                self.default_value = exrex.getone(patterns[0])
            else:
                str_len = random.randint(self.min_val, self.max_val)
                self.default_value= ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=str_len))

        super(String, self).__init__(name=name, default_value=self.default_value, *args, **kwargs)



    def mutations(self, default_value):
        last_val = None
        if self.seed is not None:
            random.seed(self.seed)

        for i in range(self.max_mutations):
            if i == 0:
                current_val = default_value
            else:
                if patterns:
                    current_val = exrex.getone(patterns[0])
                else:
                    str_len = random.randint(self.min_val, self.max_val)
                    current_val = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=str_len))

            if last_val == current_val:
                continue

            last_val = current_val
            yield current_val

    def encode (self, value, mutation_context=None):
        return value.encode()

class UInt8(Int):
    uint8_max = 2 ** 8 - 1
    uint8_min = 0

    def __init__(
            self,
            name=None,
            default_value=None,
            min_val=uint8_min,
            max_val=uint8_max,
            max_mutations=1000,
            seed=None,
            *args,
            **kwargs
    ):
        if min_val == "min":
            min_val = UInt8.uint8_min
        else:
            min_val = int(min_val)

        if max_val == "max":
            max_val = UInt8.uint8_max
        else:
            max_val = int(max_val)

        if min_val < UInt8.uint8_min:
            raise ValueError("min value too low for uint8 type")
        if max_val > UInt8.uint8_max:
            raise ValueError("max value too big for uint8 type")

        super(UInt8, self).__init__(name=name, default_value=default_value, min_val=min_val, max_val=max_val,
                max_mutations=max_mutations, seed=seed, *args, **kwargs)

class UInt16(Int):
    uint16_max = 2 ** 16 -1
    uint16_min = 0

    def __init__(
            self,
            name=None,
            default_value=None,
            min_val=uint16_min,
            max_val=uint16_max,
            max_mutations=1000,
            seed=None,
            *args,
            **kwargs
    ):
        if min_val == "min":
            min_val = UInt16.uint16_min
        else:
            min_val = int(min_val)

        if max_val == "max":
            max_val = UInt16.uint16_max
        else:
            max_val = int(max_val)

        if min_val < UInt16.uint16_min:
            raise ValueError("min value too low for uint16 type")
        if max_val > UInt16.uint16_max:
            raise ValueError("max value too big for uint16 type")

        super(UInt16, self).__init__(name=name, default_value=default_value, min_val=min_val, max_val=max_val,
                max_mutations=max_mutations, seed=seed, *args, **kwargs)

class UInt32(Int):
    uint32_max = 2 ** 32 -1
    uint32_min = 0

    def __init__(
            self,
            name=None,
            default_value=None,
            min_val=uint32_min,
            max_val=uint32_max,
            max_mutations=1000,
            seed=None,
            *args,
            **kwargs
    ):
        if min_val == "min":
            min_val = UInt32.uint32_min
        else:
            min_val = int(min_val)

        if max_val == "max":
            max_val = UInt32.uint32_max
        else:
            max_val = int(max_val)

        if min_val < UInt32.uint32_min:
            raise ValueError("min value too low for uint32 type")
        if max_val > UInt32.uint32_max:
            raise ValueError("max value too big for uint32 type")

        super(UInt32, self).__init__(name=name, default_value=default_value, min_val=min_val, max_val=max_val,
                max_mutations=max_mutations, seed=seed, *args, **kwargs)

class UInt64(Int):
    uint64_max = 2 ** 64 - 1
    uint64_min = 0

    def __init__(
            self,
            name=None,
            default_value=None,
            min_val=uint64_min,
            max_val=uint64_max,
            max_mutations=1000,
            seed=None,
            *args,
            **kwargs
    ):
        if min_val == "min":
            min_val = UInt64.uint64_min
        else:
            min_val = int(min_val)

        if max_val == "max":
            max_val = UInt64.uint64_max
        else:
            max_val = int(max_val)

        if min_val < UInt64.uint64_min:
            raise ValueError("min value too low for uint64 type")
        if max_val > UInt64.uint64_max:
            raise ValueError("max value too big for uint64 type")

        super(UInt64, self).__init__(name=name, default_value=default_value, min_val=min_val, max_val=max_val,
                max_mutations=max_mutations, seed=seed, *args, **kwargs)

class Union(boofuzz.Fuzzable):
    def __init__(
        self,
        name=None,
        children=[],
        seed=None,
        *args,
        **kwargs
    ):

        self.children = children
        super(Union, self).__init__(name=name, *args, **kwargs)

    def mutations(self, default_value):
        child = random.choice(self.children)
        return child.mutations(child.default_value)

    def encode (self, value, mutation_context=None):
        return value.encode()

yang_boofuzz_map = {libyang.Type.INT8: Int8,
            libyang.Type.INT16: Int16,
            libyang.Type.INT32: Int32,
            libyang.Type.INT64: Int64,
            libyang.Type.STRING: String,
            libyang.Type.UNION: Union,
            libyang.Type.UINT8: UInt8,
            libyang.Type.UINT16: UInt16,
            libyang.Type.UINT32: UInt32,
            libyang.Type.UINT64: UInt64
}
