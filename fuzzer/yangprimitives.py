import boofuzz
import random

class Int(boofuzz.Fuzzable):
    def __init__(
            self,
            name=None,
            default_value=0,
            i_min=0
            i_max=1
            max_mutations=1000,
            seed=None,
            *args,
            **kwargs
    ):
        super(Int, self).__init__(name=name, default_value=str(default_value), *args, **kwargs)

        self.i_min = i_min
        self.i_max = i_max
        self.max_mutations = max_mutations
        self.seed = seed

    def mutations(self, default_value):
        last_vale = None
        if self.seed is not None:
            random.seed(self.seed)
        
        for i in range(self.max_mutations):
            if i == 0:
                current_val = default_value
            else:
                current_val = random.randint(self.i_min, self.i_max)

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
            default_value=0,
            i_min=Int8.int8_min,
            i_max=Int8.int8_max,
            max_mutations=1000,
            seed=None,
            *args,
            **kwargs
    ):
        if i_min < Int8.int8_min:
            raise ValueError("min value too low for int8 type")

        if i_max > Int8.int8_max:
            raise ValueError("max value too big for int8 type")

        super(Int8, self).__init__(name=name, default_value=str(default_value), i_min=i_min, i_max=i_max,
                max_mutations=max_mutations, seed=seed, *args, **kwargs)

class Int16(Int):
    int16_max = 2 ** 15 -1
    int16_min = -2 ** 15

    def __init__(
            self,
            name=None,
            default_value=0,
            i_min=Int16.int16_min,
            i_max=Int16.int16_max,
            max_mutations=1000,
            seed=None,
            *args,
            **kwargs
    ):
        if i_min < Int16.int16_min:
            raise ValueError("min value too low for int16 type")

        if i_max > Int16.int16_max:
            raise ValueError("max value too big for int16 type")

        super(Int16, self).__init__(name=name, default_value=str(default_value), i_min=i_min, i_max=i_max,
                max_mutations=max_mutations, seed=seed, *args, **kwargs)

class Int32(Int):
    int32_max = 2 ** 31 -1
    int32_min = -2 ** 31

    def __init__(
            self,
            name=None,
            default_value=0,
            i_min=Int32.int32_min,
            i_max=Int32.int32_max,
            max_mutations=1000,
            seed=None,
            *args,
            **kwargs
    ):
        if i_min < Int32.int32_min:
            raise ValueError("min value too low for int32 type")

        if i_max > Int32.int32_max:
            raise ValueError("max value too big for int32 type")

        super(Int32, self).__init__(name=name, default_value=str(default_value), i_min=i_min, i_max=i_max,
                max_mutations=max_mutations, seed=seed, *args, **kwargs)

class Int64(Int):
    int64_max = 2 ** 63 -1
    int64_min = -2 ** 63

    def __init__(
            self,
            name=None,
            default_value=0,
            i_min=Int64.int64_min,
            i_max=Int64.int64_max,
            max_mutations=1000,
            seed=None,
            *args,
            **kwargs
    ):
        if i_min < Int64.int64_min:
            raise ValueError("min value too low for int64 type")

        if i_max > Int64.int64_max:
            raise ValueError("max value too big for int64 type")

        super(Int64, self).__init__(name=name, default_value=str(default_value), i_min=i_min, i_max=i_max,
                max_mutations=max_mutations, seed=seed, *args, **kwargs)

class UInt8(Int):
    uint8_max = 2 ** 8 - 1
    uint8_min = 0

    def __init__(
            self,
            name=None,
            default_value=0,
            i_min=UInt8.uint8_min,
            i_max=UInt8.uint8_max,
            max_mutations=1000,
            seed=None,
            *args,
            **kwargs
    ):
        if i_min < UInt8.uint8_min:
            raise ValueError("min value too low for uint8 type")
        if i_max > UInt8.uint8_max:
            raise ValueError("max value too big for uint8 type")

        super(UInt8, self).__init__(name=name, default_value=str(default_value), i_min=i_min, i_max=i_max,
                max_mutations=max_mutations, seed=seed, *args, **kwargs)

class UInt16(Int):
    uint16_max = 2 ** 16 -1
    uint16_min = 0

    def __init__(
            self,
            name=None,
            default_value=0,
            i_min=UInt16.uint16_min,
            i_max=UInt16.uint16_max,
            max_mutations=1000,
            seed=None,
            *args,
            **kwargs
    ):
        if i_min < UInt16.uint16_min:
            raise ValueError("min value too low for uint16 type")
        if i_max > UInt16.uint16_max:
            raise ValueError("max value too big for uint16 type")

        super(UInt16, self).__init__(name=name, default_value=str(default_value), i_min=i_min, i_max=i_max,
                max_mutations=max_mutations, seed=seed, *args, **kwargs)

class UInt32(Int):
    uint32_max = 2 ** 32 -1
    uint32_min = 0

    def __init__(
            self,
            name=None,
            default_value=0,
            i_min=UInt32.uint32_min,
            i_max=UInt32.uint32_max,
            max_mutations=1000,
            seed=None,
            *args,
            **kwargs
    ):
        if i_min < UInt32.uint32_min:
            raise ValueError("min value too low for uint32 type")
        if i_max > UInt32.uint32_max:
            raise ValueError("max value too big for uint32 type")

        super(UInt32, self).__init__(name=name, default_value=str(default_value), i_min=i_min, i_max=i_max,
                max_mutations=max_mutations, seed=seed, *args, **kwargs)

class UInt64(Int):
    uint64_max = 2 ** 64 - 1
    uint64_min = 0

    def __init__(
            self,
            name=None,
            default_value=0,
            i_min=UInt64.uint64_min,
            i_max=UInt64.uint64_max,
            max_mutations=1000,
            seed=None,
            *args,
            **kwargs
    ):
        if i_min < UInt64.uint64_min:
            raise ValueError("min value too low for uint64 type")
        if i_max > UInt64.uint64_max:
            raise ValueError("max value too big for uint64 type")

        super(UInt64, self).__init__(name=name, default_value=str(default_value), i_min=i_min, i_max=i_max,
                max_mutations=max_mutations, seed=seed, *args, **kwargs)
