import pymssql
import pandas

class Caminhao:
    codTransportadora=''
    NroEntregas=0
    PesoBruto=0.0
    Litros=0.0
    PesoMax=0.0


def getValueByName(row, name):
    for key in row:
        if key.strip().upper() == name.strip().upper():
            return row[key]

    return None


class LeitorCaminhoes:
    conn = None

    def __init__(self, open=True):
        if open:
            self.open()

    def open(self):
        self.conn = pymssql.connect(host=r'10.0.0.201', port=1433, user=r'user', password=r'28021990',
                                    database=r'logistec')

    def close(self):
        return self.conn.close()

    def getDadosEntregas(self, codTransp):
        df = pandas.read_sql('''select ec.CodPedido as 'Cod. Ped.', C.NOMECLIENTE as 'Cliente', C.CIDADE as 'Cidade', Ec.PesoBruto as 'Peso'
                                from vwEntregasCaminhoes ec
                                inner join CLIENTE C on C.CODCLIENTE = ec.CodCliente
                                where ec.codtransportadora = '%s' 
                                order by PesoBruto desc ''' % codTransp.zfill(6),
                             self.conn)

        return df

    def getDadosCaminhao(self, codTransp):
        cursor = self.conn.cursor(as_dict=True)

        cursor.execute('select * from vwCaminhoes where codtransportadora = %s', codTransp.zfill(6))

        caminhao = Caminhao()
        caminhao.codTransportadora = codTransp.zfill(6)

        for row in cursor:
            caminhao = Caminhao()
            caminhao.codTransportadora = getValueByName(row, 'CODTRANSPORTADORA')
            caminhao.NroEntregas = getValueByName(row, 'NroEntregas')
            caminhao.PesoBruto = getValueByName(row, 'PesoBruto')
            caminhao.Litros = getValueByName(row, 'litros')
            caminhao.PesoMax = getValueByName(row, 'PesoMax')
            #caminhoes.append(caminhao)

        return caminhao







