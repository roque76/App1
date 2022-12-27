import sqlite3
import itertools
class Conexion():
    def __init__(self):
        self.conexion = sqlite3.connect('Inventario.db')

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
    
    def fact_inv(self,ref,name,mat,group,prec,cant):
        cursor = self.conexion.cursor()
        cursor.execute(f"INSERT INTO FACTURAS (REF,NOMBRE,MATERIAL,GRUPO,PRECIO_VENTA,CANTIDAD)VALUES('{ref}','{name}','{mat}','{group}','{prec}','{cant}')")
        self.conexion.commit()
        self.tot_val()
        cursor.close()
        
    
    def show_fact(self):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT REF,NOMBRE,MATERIAL,GRUPO,PRECIO_VENTA,CANTIDAD,VALOR_TOTAL,IVA FROM FACTURAS")
        fact = cursor.fetchall()
        cursor.close()
        return fact
    
    def fact_group(self,group):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT REF,NOMBRE,MATERIAL,GRUPO,PRECIO_VENTA,CANTIDAD,VALOR_TOTAL,IVA FROM FACTURAS WHERE GRUPO =?",(group,))
        filt = cursor.fetchall()
        cursor.close()
        self.tot_val()
        return filt
    
    def tot_val(self):
        cursor = self.conexion.cursor()
        cursor.execute("UPDATE FACTURAS SET VALOR_TOTAL=PRECIO_VENTA*CANTIDAD")
        self.conexion.commit()
        cursor.close()