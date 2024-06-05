class Stack():
    def __init__(self, size):
        try :
            self.max_size = int(size)
            if size<=0 or size > 50000 : raise Exception()
        except:
            raise Exception("Ошибка инициализации стека")
        self.memory = [0 for x in range(self.max_size)]
        self.top = 0

    def push(self, value):
        if self.top < self.max_size:
            self.memory[self.top] = value
            self.top += 1
        else:
            raise Exception("Стек заполнен")

    def pop(self):
        if self.top > 0:
            self.top -= 1
            return self.memory[self.top]
        else:
            raise Exception('Стек пуст')

    def clear(self):
        self.memory = [0 for x in range(self.max_size)]
        self.top = 0

    def stack_info(self):
        print()
        for i in range(self.max_size-1,-1,-1) :            #   stack_data in self.memory[::-1]:
            stack_data = self.memory[i]
            if i < self.top :
                print(i,stack_data)
            else :
                print(i,'--- <==') if i == self.top else print(i, "---")
        if self.top == self.max_size : print("stack is full")

st1 = Stack(6)
st1.push(123)
st1.push(456)
st1.stack_info()
st1.pop()
st1.pop()
