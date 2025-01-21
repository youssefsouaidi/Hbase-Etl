import happybase


def scan_hbase_table(table_name):
    try:
        connection = happybase.Connection('localhost')
        connection.open()

        table = connection.table(table_name)

        print(f"Scanning table: {table_name}\n")

        # Scanner les données
        for key, data in table.scan():
            print(f"Row Key: {key.decode('utf-8')}")
            for column, value in data.items():
                print(f"    {column.decode('utf-8')} : {value.decode('utf-8')}")
            print("-" * 40)

    except Exception as e:
        print(f"Erreur lors du scan de la table {table_name} : {e}")
    finally:
        connection.close()


table_name = 'userdata'
scan_hbase_table(table_name)
