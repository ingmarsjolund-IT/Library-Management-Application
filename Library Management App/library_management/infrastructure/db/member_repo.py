
from typing import Optional, List
from infrastructure.db.database import get_connection, init_db
from domain.models import Member


class MemberRepo:
    def __init__(self):
        init_db()
        self.conn = get_connection()
        self.cur = self.conn.cursor()

    sql_insert = "INSERT INTO members (member_id, member_name, member_contact, member_type) VALUES (?, ?, ?, ?)"
    sql_insert_auto = "INSERT INTO members (member_name, member_contact, member_type) VALUES (?, ?, ?)"
    sql_selectall = "SELECT member_id, member_name, member_contact, member_type FROM members ORDER BY member_id"
    sql_selectone = "SELECT member_id, member_name, member_contact, member_type FROM members WHERE member_id = ?"
    sql_update = "UPDATE members SET member_name = ?, member_contact = ?, member_type = ? WHERE member_id = ?"
    sql_delete = "DELETE FROM members WHERE member_id = ?"

    def selectall_members(self) -> List[Member]:
        self.cur.execute(self.sql_selectall)
        rows = self.cur.fetchall()
        return [Member.from_row(row) for row in rows]

    def selectone_member(self, member_id: int) -> Optional[Member]:
        self.cur.execute(self.sql_selectone, (member_id,))
        row = self.cur.fetchone()
        return None if row is None else Member.from_row(row)

    def insert_member(self, member: Member, force_id: bool = True) -> int:
        if force_id and member.member_id:
            self.cur.execute(self.sql_insert, (member.member_id, member.member_name, member.member_contact, member.member_type))
        else:
            self.cur.execute(self.sql_insert_auto, (member.member_name, member.member_contact, member.member_type))
        self.conn.commit()
        return int(self.cur.lastrowid)

    def update_member(self, member: Member) -> int:
        self.cur.execute(self.sql_update, (member.member_name, member.member_contact, member.member_type, member.member_id))
        self.conn.commit()
        return self.cur.rowcount

    def delete_member(self, member_id: int) -> int:
        self.cur.execute(self.sql_delete, (member_id, ))
        self.conn.commit()
        return self.cur.rowcount

    def close(self) -> None:
        try:
            self.cur.close()
        finally:
            self.conn.close()
