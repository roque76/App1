import sqlite3
import itertools
import datetime
class Conexion():
    def __init__(self):
        self.conexion = sqlite3.connect('Inventario.db')
        self.bill_ids= itertools.count(start=1,step=1)

    def show_inv(self):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT REFERENCIA,NOMBRE,MATERIAL,PRECIO_VENTA,CANTIDAD,GRUPO FROM INVENTARIO")
        inventory = cursor.fetchall()
        cursor.close()
        return inventory

    def group_inv(self,group):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT REFERENCIA,NOMBRE,MATERIAL,PRECIO_VENTA,CANTIDAD,GRUPO FROM INVENTARIO WHERE GRUPO=?",(group,))
        inventory = cursor.fetchall()
        cursor.close()
        return inventory
    
    def ref_inv(self,ref):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT REFERENCIA,NOMBRE,MATERIAL,GRUPO,PRECIO_VENTA,CANTIDAD FROM INVENTARIO WHERE REFERENCIA=?",(ref,))
        inventory = cursor.fetchall()
        cursor.close()
        return inventory
    
    def new_fact(self):
        global bill_id,last_id
        try:
            with open ("ID.txt") as f:
                last_id = int(f.read())
        except FileNotFoundError:
            last_id = 1
        
        bill_id = itertools.count(start=last_id,step=1)
        bill_id = next(bill_id)
        
    
    def close_bill(self):
        global bill_id
        now=datetime.datetime.now()
        date = now.date()
        time = now.time()
        billid = str(bill_id+1)
        cursor = self.conexion.cursor()
        cursor.execute("SELECT SUM(VALOR_TOTAL) FROM FACTURAS WHERE NUM_FACT=?",(bill_id,))
        filt = cursor.fetchone()
        bill = filt[0]
        cursor.execute("SELECT SUM(CANTIDAD) FROM FACTURAS WHERE NUM_FACT=?",(bill_id,))
        filterd = cursor.fetchone()
        cant = filterd[0]
        cursor.execute(f"INSERT INTO CONDENSADO (VAL_TOT,NUM_FACT,FECHA,TIEMPO,CANTIDAD)VALUES('{bill}','{bill_id}','{date}','{time}','{cant}')")
        with open("ID.txt", "w") as f:
            f.write(billid)
        self.conexion.commit()
        self.iva_factrs()
        cursor.close()

    def iva_factrs(self):
        cursor = self.conexion.cursor()
        cursor.execute("UPDATE CONDENSADO SET IVA=VAL_TOT*0.19")
        self.conexion.commit()
        cursor.close()
        
    def fact_inv(self,ref,name,mat,group,prec,cant):
        now = datetime.datetime.now()
        date = now.date()
        time = now.time()
        cursor = self.conexion.cursor()
        cursor.execute(f"INSERT INTO FACTURAS (REF,NOMBRE,MATERIAL,GRUPO,PRECIO_VENTA,CANTIDAD,NUM_FACT,FECHA,TIEMPO)VALUES('{ref}','{name}','{mat}','{group}','{prec}','{cant}','{bill_id}','{date}','{time}')")
        self.conexion.commit()
        self.tot_val()
        cursor.close()
        
    
    def show_fact(self):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT REF,NOMBRE,MATERIAL,GRUPO,PRECIO_VENTA,CANTIDAD,VALOR_TOTAL,IVA,FECHA,NUM_FACT FROM FACTURAS")
        fact = cursor.fetchall()
        cursor.close()
        return fact
    
    def fact_num_fact(self,num_fact):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT REF,NOMBRE,MATERIAL,GRUPO,PRECIO_VENTA,CANTIDAD,VALOR_TOTAL,IVA,FECHA,NUM_FACT FROM FACTURAS WHERE NUM_FACT =?",(num_fact,))
        filt = cursor.fetchall()
        cursor.close()
        self.tot_val()
        return filt
    
    def tot_val(self):
        cursor = self.conexion.cursor()
        cursor.execute("UPDATE FACTURAS SET VALOR_TOTAL=PRECIO_VENTA*CANTIDAD")
        self.conexion.commit()
        cursor.execute("UPDATE FACTURAS SET IVA=VALOR_TOTAL*0.19")
        self.conexion.commit()
        cursor.close()