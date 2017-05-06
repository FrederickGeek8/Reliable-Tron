def array_to_string(array):
    string = str(array)
    return string[1:(len(string)-1)].replace(' ', '')

if __name__ == '__main__':
    array = [1,2,3]
    print(array_to_string(array))
