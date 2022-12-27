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
    
    def search(self,name):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT*FROM INVENTARIO WHERE NOMBRE=?",(name,))
        search = cursor.fetchall()
        cursor.close()
        return search
    
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