import random


class RandBy(object):
    """
        We already have std-random, why we need this?
    """

    def rand_by(self, seq, choice=None, percentage=100):
        """
            Input a right weight list, the value should be 0 ~ 1
            Example: [0, 0.1, 0.2, 0.3,0.4]
        """
        if not isinstance(seq, list):
            raise ValueTypeError("Please Input a List as the first param!")

        if sum(seq) != 1:
            raise ValueError("The sum of seq must equal 1")
        
        if choice:
            pass
        else:
            weight_area = [i * seq[i] * percentage for i in range(len(seq))]
            weight_list = [[j] * int(weight_area[j]) for j in range(len(weight_area))]
            weight_area_to_index = map(lambda x: [x]*len(x), weight_list)
            weight_list_area = reduce(lambda x,y: x+y, weight_list)
            target = random.choice(weight_list_area)
            return target



if __name__ == '__main__':
    rb = RandBy()
    a=[0,0.1,0.4,0.5]
    for i in range(10):
        print(rb.rand_by(a))


