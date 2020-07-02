
import itertools



def compose_y(no):
    print(no)
    d = []
    for item in itertools.product(*no):
        d.append(item)

    return d



if __name__ == '__main__':
    no=[{"len": 1, "cp": ["4","3","2"]}, {"len": 1, "cp": ["0"]}, {"len": 1, "cp": ["2"]}, {"len": 1, "cp": ["7"]},
            {"len": 1, "cp": ["6"]}]

    res = compose_y([ item['cp'] for item in no])
    print(res)
