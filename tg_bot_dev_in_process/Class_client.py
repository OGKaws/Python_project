class Client():
    def __init__(self,client_name):
        self.name = client_name
        self.paid_training = 0
        self.done_training = 0

    #def Client_new(self,obj_name,new_client_name):
    #    obj_name = Client(new_client_name)

    def Client_paid_training(self, session_paid):
        self.paid_training = session_paid

    def Client_comp_training(self):
        self.paid_training -= 1
        self.done_training += 1

    def Client_info(self):
        print(self.name, 'осталось оплачено', self.paid_training,'\nпройдено тренировок', self.done_training)

    def Client_to_dict(self):
        return {self.name : {'paid lessons ' : self.paid_training}}
