import psycopg2


def create_db(conn) -> None:
    with conn.cursor() as cur:
        cur.execute('''
        CREATE TABLE IF NOT EXISTS clients (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(40) NOT NULL,
        last_name VARCHAR(40) NOT NULL,
        email VARCHAR(40) UNIQUE NOT NULL 
        );
        CREATE TABLE IF NOT EXISTS phones (
        client_id INTEGER NOT NULL REFERENCES clients (id) ON DELETE CASCADE,
        phone VARCHAR(40) UNIQUE NOT NULL,
        is_active BOOLEAN DEFAULT TRUE,
        CONSTRAINT client_phone_pk PRIMARY KEY (client_id, phone)
        );
        ''')
        print('Созданы таблицы в БД  - clients, phones')


def add_client(conn, first_name: str, last_name: str, email: str, phones: tuple = None) -> None:
    with conn.cursor() as cur:
        cur.execute('''
        INSERT INTO clients (first_name, last_name, email)
        VALUES (%s, %s, %s) RETURNING id;
        ''', (first_name, last_name, email))
        client_id = cur.fetchone()[0]
        print(f'Добавлен новый клиент c id - {client_id}')
        if phones:
            for phone in phones:
                add_phone(conn, client_id, phone)


def add_phone(conn, client_id: int, phone: str) -> None:
    with conn.cursor() as cur:
        cur.execute('''
        INSERT INTO phones (client_id, phone)
        VALUES (%s, %s);
        ''', (client_id, phone))
        print(f'Клиенту с id {client_id} добавлен телефон - {phone}')


def change_client(conn, client_id: int, first_name: str = None,
                  last_name: str = None, email: str = None, phones: tuple = None) -> None:
    data_dict = {'first_name': first_name, 'last_name': last_name, 'email': email}
    sql_set = ", ".join([f"{k} = '{v}'" for k, v in data_dict.items() if v])
    sql_request = f'''
    UPDATE clients SET {sql_set}
    WHERE id = {client_id};
    '''
    with conn.cursor() as cur:
        if sql_set:
            cur.execute(sql_request)
        if phones:
            cur.execute('''
            SELECT phone FROM phones
            WHERE client_id=%s AND is_active=TRUE;
            ''', (client_id,))
            client_phones = cur.fetchall()
            if len(client_phones) == len(phones):
                for i, phone in enumerate(client_phones):
                    cur.execute('''
                                UPDATE phones SET phone=%s
                                WHERE client_id=%s AND phone=%s AND is_active=TRUE;
                                ''', (phones[i], client_id, phone[0]))
    print(f'Изменения в данные клиента с id {client_id} - внесены')


def delete_phone(conn, client_id: int, phone: str) -> None:
    with conn.cursor() as cur:
        cur.execute('''
        SELECT phone FROM phones
        WHERE client_id=%s AND phone=%s;
        ''', (client_id, phone))
        client_phones = cur.fetchall()
        if client_phones:
            cur.execute('''
            UPDATE phones SET is_active=FALSE
            WHERE client_id=%s AND phone=%s;
            ''', (client_id, phone))
            print(f'Телефон {phone} клиента с id {client_id} - удален (не активен)')
        else:
            print(f'Телефон {phone} у клиента с id {client_id} - отсутствует')


def delete_client(conn, client_id: int) -> None:
    with conn.cursor() as cur:
        cur.execute('''
        DELETE FROM clients WHERE id=%s;
        ''', (client_id,))
        print(f'Клиент с id {client_id} и все данные о нем из БД - удалены (безвозвратно)')


def find_client(conn, first_name: str = None, last_name: str = None,
                email: str = None, phone: str = None) -> None:
    data_dict = {'first_name': first_name, 'last_name': last_name, 'email': email, 'phone': phone}
    sql_where = " AND ".join([f"{k} = '{v}'" for k, v in data_dict.items() if v])
    sql_request = f'''
    SELECT DISTINCT cl.id, cl.first_name, cl.last_name FROM phones AS ph
    JOIN clients AS cl ON ph.client_id = cl.id
    WHERE {sql_where};
    '''
    with conn.cursor() as cur:
        cur.execute(sql_request)
        print(f'Найдено: {cur.fetchall()}')


if __name__ == '__main__':
    with psycopg2.connect(database='phones', user='postgres', password='123456') as connect:
        try:
            create_db(connect)
            add_client(connect, first_name='Иван', last_name='Иванов', email='ivanov@mail.ru',
                       phones=('+79251234567', '+79252345678'))
            add_client(connect, first_name='Иван', last_name='Петров', email='petrov@mail.ru')
            add_client(connect, first_name='Петр', last_name='Сидоров', email='sidorov@mail.ru')
            add_client(connect, first_name='Василий', last_name='Сидоров', email='v.sidorov@mail.ru',
                       phones=('+79260987654',))
            add_phone(connect, client_id=2, phone='+79163456789')
            add_phone(connect, client_id=2, phone='+79999456789')
            add_phone(connect, client_id=3, phone='+79164567890')
            delete_phone(connect, client_id=1, phone='+79251234567')
            change_client(connect, client_id=2, last_name='Ожогов', email='i.ozh@mail.ru',
                          phones=('+43', '+53'))
            delete_client(connect, client_id=1)
            find_client(connect, first_name='Иван', last_name='Ожогов')
        except psycopg2.Error as er:
            print(f'ERROR: {er}')
    connect.close()
