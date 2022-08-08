import pytest


"""
STEPS TO RUN TESTs FOR PROGRAM(s) GIVEN BELOW:
    - open shell/cmd window at same directory.
    - run `pytest -s programs.py` command to run all tests
    - the test result(s) will be seen on console/cmd window
"""


def fzbz(num):
    """
        @description: fn to substitute a number (in given range)  multiple of 3 with 'fizz' and 5 with 'buzz'
                      & multiple of 3 and 5 with 'fizz buzz'
        @param num: integer set bar
        @return:    prints the output from 0 to 'num' on screen after value substitution
    """
    assert isinstance(num, int)
    assert num > 0
    for e in range(1, num+1):
        if e%3 == 0 and e%5 ==0:
            print("fizz buzz")
        elif e%3 == 0:
            print('fizz')
        elif e%5 == 0:
            print('buzz')
        else:
            print(e)



def fibo(num):
    """
     @description: fn generates the fibonacci series from 0 to 'num'
     @param num: integer value, i.e. equal to number of elements of the output series
     @return: fibonacci series as list
    """
    assert isinstance(num, int)
    assert num > 0
    f_series = [0, 1]
    if num == 1:
        return [0]
    if num == 2:
        return f_series

    for num in range(3, num+1):
        temp= f_series[-1] + f_series[-2]
        f_series.append(temp)
    return f_series



def matcher(text):
    """
     @description: finds the number of repetitive words in a string
     @param text: input string value
     @return:  a dictionary with word(s) as key(s) and number of repetition as its value
    """
    assert isinstance(text, str)
    # remove additional space from input string
    text = " ".join(text.split())
    assert text != ""
    out = {}
    text = text.lower()
    # getting available words as list
    words = text.split(' ')
    for word in words:
        if out.get(word) is not None:
            out[word] += 1
        else:
            out[word] = 1
    return out




@pytest.mark.parametrize("num",[1,2,11])
def test_fzbz(num):
    fzbz(num)


@pytest.mark.parametrize("num",[1,2,11])
def test_fibo(num):
    series = fibo(num)
    print(series)


@pytest.mark.parametrize(
"text",[
    "Hi how are things? How are you? Are you a developer? I am also a developer",
    "this is a test case for matching and counting words. This test case is free to use",
    "If it is working properly then it word has a value of 2"
    ]
)
def test_matcher(text):
    output = matcher(text)
    print(output)
