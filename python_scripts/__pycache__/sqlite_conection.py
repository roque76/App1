import sqlite3

class Conect():
    def __init__(self):
        self.conexion = sqlite3.connect('Inventario.db')
    
    def register(self,ref,name,mat,cant,prec,compra,group):
        cursor = self.conexion.cursor()
        bd = f'''INSERT INTO INVENTARIO (REFERENCIA,NOMBRE,MATERIAL,PRECIO_VENTA,COMPRA,CANTIDAD,GRUPO)
        VALUES('{ref}','{name}','{mat}','{prec}','{compra}','{cant}','{group}')'''
        cursor.execute(bd)
        self.conexion.commit()
        cursor.close()
        self.updt_util()
    
    def show_inv(self):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT* FROM INVENTARIO")
        registro = cursor.fetchall()
        cursor.close()
        return registro
    
    def delete(self,name):
        cursor = self.conexion.cursor()
        cursor.execute("DELETE FROM INVENTARIO WHERE NOMBRE=?",(name,))
        self.conexion.commit()
        cursor.close()
    
    def update(self,id_,ref,name,mat,prec,compra,cant,group):
        cursor = self.conexion.cursor()
        bd = 'UPDATE INVENTARIO SET REFERENCIA="{}",NOMBRE="{}",MATERIAL="{}",PRECIO_VENTA="{}",COMPRA="{}",CANTIDAD="{}", GRUPO="{}" WHERE ID={}'.format(ref,name,mat,prec,compra,cant,group,id_)
        cursor.execute(bd)
        a = cursor.rowcount
        self.conexion.commit()
        cursor.close()
        self.updt_util()
        return a    
        
    def updt_util(self):
        cursor = self.conexion.cursor()
        cursor.execute("UPDATE INVENTARIO SET UTILIDAD=PRECIO_VENTA-COMPRA")
        self.conexion.commit()
        cursor.close()

    def gr_db(self,group):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT*FROM INVENTARIO WHERE GRUPO=?",(group,))
        inv = cursor.fetchall()
        cursor.close()
        return inv

    def ref_db(self,ref):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT*FROM INVENTARIO WHERE REFERENCIA=?",(ref,))
        inv = cursor.fetchall()
        cursor.close()
        return inv
    def name_db(self,name):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT*FROM INVENTARIO WHERE NOMBRE=?",(name,))
        inv = cursor.fetchall()
        cursor.close()
        return inv
    def mat_db(self,mat):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT*FROM INVENTARIO WHERE MATERIAL=?",(mat,))
        inv = cursor.fetchall()
        cursor.close()
        return inv
    def buyed_db(self,buyd):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT*FROM INVENTARIO WHERE COMPRA =?",(buyd,))
        inv = cursor.fetchall()
        cursor.close()
        return inv
    def utils_db(self,ut):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT*FROM INVENTARIO WHERE UTILIDAD=?",(ut,))
        inv = cursor.fetchall()
        cursor.close()
        return inv
    def cant_db(self,cant):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT*FROM INVENTARIO WHERE CANTIDAD=?",(cant,))
        inv = cursor.fetchall()
        cursor.close()
        return inv
    def prec_db(self,prec):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT*FROM INVENTARIO WHERE PRECIO_VENTA=?",(prec,))
        inv = cursor.fetchall()
        cursor.close()
        return inv
    def show_fact(self):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM FACTURAS")
        inv = cursor.fetchall()
        cursor.close()
        return inv

    def id_fact(self,id):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT* FROM FACTURAS WHERE ID=?",(id,))
        inv = cursor.fetchall()
        cursor.close()
        return inv

    def ref_fact(self,ref):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT*FROM FACTURAS WHERE REF=?",(ref,))
        inv = cursor.fetchall()
        cursor.close()
        return inv
    
    def name_fact(self,name):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT*FROM FACTURAS WHERE NOMBRE=?",(name,))
        inv = cursor.fetchall()
        cursor.close()
        return inv

    def mat_fact(self,mat):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT*FROM FACTURAS WHERE MATERIAL=?",(mat,))
        inv = cursor.fetchall()
        cursor.close()
        return inv

    def group_fact(self,group):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT* FROM FACTURAS WHERE GRUPO=?",(group,))
        inv = cursor.fetchall()
        cursor.close()
        return inv
    
    def price_fact(self,price):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT* FROM FACTURAS WHERE PRECIO_VENTA=?",(price,))
        inv = cursor.fetchall()
        cursor.close()
        return inv

    def cant_fact(self,cant):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT* FROM FACTURAS WHERE CANTIDAD=?",(cant,))
        inv = cursor.fetchall()
        cursor.close()
        return inv

    def tot_fact(self,tot_val):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT* FROM FACTURAS WHERE VALOR_TOTAL=?",(tot_val,))
        inv = cursor.fetchall()
        cursor.close()
        return inv
    
    def iva_fact(self,iva):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT* FROM FACTURAS WHERE IVA=?",(iva,))
        inv = cursor.fetchall()
        cursor.close()
        return inv
    
    def num_fact(self,num_fact):
        cursor = self.conexion.cursor()
        cursor.execute(f"SELECT* FROM FACTURAS WHERE NUM_FACT={num_fact}")
        inv = cursor.fetchall()
        cursor.close()
        return inv
    
    def date_fact(self,date):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT* FROM FACTURAS WHERE FECHA=?",(date))
        inv = cursor.fetchall()
        cursor.close()
        return inv
    
    def time_fact(self,time):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT* FROM FACTURAS WHERE TIEMPO=?",(time,))
        inv = cursor.fetchall()
        cursor.close()
        return inv

    def show_cond(self):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT*FROM CONDENSADO")
        inv = cursor.fetchall()
        cursor.close()
        return inv
    
    def id_cond(self,id):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT*FROM CONDENSADO WHERE ID=?",(id,))
        inv = cursor.fetchall()
        cursor.close()
        return inv
    
    def valtot_connd(self,val):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT*FROM CONDENSADO WHERE VAL_TOT=?",(val,))
        inv = cursor.fetchall()
        cursor.close()      
        return inv
    
    def numfact_cond(self,num):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT*FROM CONDENSADO WHERE NUM_FACT=?",(num,))
        inv = cursor.fetchall()
        cursor.close()
        return inv
    
    def cant_cond(self,cant):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT*FROM CONDENSADO WHERE CANTIDAD=?",(cant,))
        inv = cursor.fetchall()
        cursor.close()
        return inv