class Maillon:
    def __init__(self, data):
        self.data = data
        self.next = None 

class LinkedList:
    def __init__(self):
        self.head = None 

    def insertAtBeginning(self, new_data):
        new_node = Maillon(new_data)
        new_node.next = self.head
        self.head = new_node

    def insertAtEnd(self, new_data):
        new_node = Maillon(new_data)
        if self.head is None:    
            self.head = new_node
            return
        
        last = self.head
        while last.next:         
            last = last.next
        last.next = new_node    

    def printList(self):
        temp = self.head
        while temp:
            print(temp.data, end=' ')
            temp = temp.next
        print()



if __name__ == '__main__':
    llist = LinkedList()

    llist.insertAtBeginning('Algo&Dev') 
    llist.insertAtBeginning('de') 
    llist.insertAtBeginning('cours')  
    llist.insertAtBeginning('Le')

    llist.printList()  
   
    llist.insertAtEnd('dure')
    llist.insertAtEnd('toute')
    llist.insertAtEnd('la journée')

    llist.printList()
