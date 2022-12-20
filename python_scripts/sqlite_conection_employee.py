import sqlite3

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
        cursor.execute("SELECT REFERENCIA,NOMBRE,MATERIAL,PRECIO_VENTA,CANTIDAD FROM INVENTARIO WHERE REFERENCIA=?",(ref,))
        inventory = cursor.fetchall()
        cursor.close()
        return inventory
    
    def fact_inv(self,ref,name,mat,group,prec,cant):
        cursor = self.conexion.cursor()
        command = f'''INSERT INTO FACTURAS (REFERENCIA,NOMBRE,MATERIAL,GRUPO,PREC_UNIT,CANTIDAD)VALUES('{ref}','{name}','{mat}','{group},'{prec}','{cant}')'''
        cursor.execute(command)
        self.conexion.commit()
        a = cursor.rowcount
        cursor.close()
        return a