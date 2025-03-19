
import mysql.connector as db
from decimal import Decimal

con = db.connect(user='root',password='1466325',host='localhost',database='myproject')
cur = con.cursor()

while True: #main loop
    print('1.Admin')
    print('2.Inventory')
    user=int(input('select the option to enter:'))
    
    if user==1: #admin block
        
        while True:
            
            print('1.Display the Bag')
            print('2.Adding Items')
            print('3.Revenue')
            option = int(input('Enter the option: '))

            if option == 1: #Display the Bag

                cur.execute('select * from mybag')#fetch and display the items and quantity
                items =cur.fetchall()
                print('items --------> quantity')
                for i in items:
                    print('{} ---------> {}'.format(i[1],i[2]))
                break
            
            elif option == 2: #Adding Items
                
                while True:
                    print('1.To add new items')
                    print('2.To add quantity for items')
                    select = int(input('Enter the option:'))
                    
                    if select == 1:
                        Sno = int(input('enter the sno: '))
                        item = input('enter the item name: ')
                        quantity = float(input('enter the quantity: '))
                        price = float(input('enter the price_per_kg: '))
                        item_no = int(input('enter the item_no: '))

                        data = (Sno, item, quantity, price, item_no, None)
                        output = cur.callproc('insertnewitems', data)

                        # Fetch the output from the OUT parameter (res)
                        print(output)  # This will print the updated result set with the OUT parameter

                        break
            elif option == 3: #Revenue 

                while True:
                    print('Revenue')
                    break


    elif user==2: #inventory block
        Inventory_active=True
        while Inventory_active:
            cur.execute('select * from mybag')#featch and display the items and price
            items_list=cur.fetchall()
            print('items',  '----->',  'price')
            for i in items_list:
                print('{} ------>  {}.00'.format(i[1],i[3]))
                
            while True:  #loop for buying items

                item=input('what do you want: ')
                query='select count(*) from mybag where items=%s'
                cur.execute(query,(item,))
                item_cnt = cur.fetchone()
                
                if item_cnt[0]>0:
                    qty=float(input('how many kgs you want: '))
                    query='select quantity from mybag where items=%s'
                    cur.execute(query,(item,))
                    qty_avilable=cur.fetchone()
                    
                    if qty<=qty_avilable[0]:
                        query='select price_per_kg from mybag where items=%s'
                        cur.execute(query,(item,))
                        price=cur.fetchone()
                        
                        qty1 =(qty_avilable[0]-qty)#remaining quantity
                        inputdata = (float(qty1),item,None)
                        output=cur.callproc('updatequantity',inputdata)#procedure that quantity
                        
                        amount=float(qty*price[0])
                        
                        data1=(item,qty,amount,None)
                        output=cur.callproc('insertitems',data1)#procedure that insert data into bill table
                        print(output)
                        ask=input('do you want buy more(yes/no):')
                        if ask=='no':
                            cur.execute('select * from bill')
                            data2=cur.fetchall()
                            cur.execute('select sum(price)from bill')
                            total_amt=cur.fetchone()
                            print('*'*5,'BILL','*'*5)
                            for i in data2:
                                print(i[0],'--',i[1],'kgs','--',i[2])
                            print('total bill is:',total_amt[0])
                            #cur.execute('delete from bill')
                            print()
                            
                            print('1.Home page')
                            print('2.Inventory')
                            enter = input('where you want to go:')
                            if enter=='1':
                                Inventory_active=False #break the outer loop and return to main loop
                                break  #break the buying loop
                            elif enter=='2': #to go to the inventory loop, so break the inner loop that go to buying items. 
                                break
          
                    else:
                        print('out of stock')
                            
                    
                else:
                    print(item,'is not available')

    else:
        print('invaild option')
        print('select correct option')
            

con.commit()
cur.close()
con.close()

 
