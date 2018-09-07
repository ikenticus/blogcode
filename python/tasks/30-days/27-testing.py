def minimum_index(seq):
    if len(seq) == 0:
        raise ValueError("Cannot get the minimum value index from an empty sequence")
    min_idx = 0
    for i in range(1, len(seq)):
        if seq[i] < seq[min_idx]:
            min_idx = i
    return min_idx


from random import randint

class TestDataEmptyArray(object):
    
    @staticmethod
    def get_array():
        # complete this function
        return []

class TestDataUniqueValues(object):
    data = set()
    while len(data) < randint(10, 50):
        data.add(randint(0, 100))    

    @staticmethod
    def get_array():
        # complete this function
        got = TestDataUniqueValues.data
        return list(got)

    @staticmethod
    def get_expected_result():
        # complete this function
        want = TestDataUniqueValues.get_array()
        return want.index(min(want))
    
class TestDataExactlyTwoDifferentMinimums(object):
    data = set()
    while len(data) < randint(10, 50):
        data.add(randint(0, 100))    
    diff = list(data)
    diff.append(min(diff))

    @staticmethod
    def get_array():
        # complete this function
        got = TestDataExactlyTwoDifferentMinimums.diff
        return list(got)
    
    @staticmethod
    def get_expected_result():
        # complete this function
        want = TestDataExactlyTwoDifferentMinimums.get_array()
        return want.index(min(want))



def TestWithEmptyArray():
    try:
        seq = TestDataEmptyArray.get_array()
        result = minimum_index(seq)
    except ValueError as e:
        pass
    else:
        assert False


def TestWithUniqueValues():
    seq = TestDataUniqueValues.get_array()
    assert len(seq) >= 2

    assert len(list(set(seq))) == len(seq)

    expected_result = TestDataUniqueValues.get_expected_result()
    result = minimum_index(seq)
    assert result == expected_result


def TestiWithExactyTwoDifferentMinimums():
    seq = TestDataExactlyTwoDifferentMinimums.get_array()
    assert len(seq) >= 2
    tmp = sorted(seq)
    assert tmp[0] == tmp[1] and (len(tmp) == 2 or tmp[1] < tmp[2])

    expected_result = TestDataExactlyTwoDifferentMinimums.get_expected_result()
    result = minimum_index(seq)
    assert result == expected_result

TestWithEmptyArray()
TestWithUniqueValues()
TestiWithExactyTwoDifferentMinimums()
print "OK"


