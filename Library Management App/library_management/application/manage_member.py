
from typing import List
from domain.models import Member, ViewMember
from infrastructure.db.member_repo import MemberRepo


class ManageMember:
    @staticmethod
    def _validate(vm: ViewMember) -> List[str]:
        errs = []
        if not vm.name.strip():
            errs.append("Member name is required.")
        if not vm.contact.strip():
            errs.append("Member contact is required.")
        if not vm.type.strip():
            errs.append("Member type is required.")
        if vm.id and not vm.id.isdigit():
            errs.append("Member ID must be an integer.")
        return errs

    @staticmethod
    def CreateMember(vm: ViewMember) -> List[str]:
        errs = ManageMember._validate(vm)
        if errs:
            return errs
        member = Member(
            member_name=vm.name.strip(),
            member_id=int(vm.id) if vm.id else 0,
            member_contact=vm.contact.strip(),
            member_type=vm.type.strip(),
        )
        repo = MemberRepo()
        try:
            repo.insert_member(member, force_id=bool(vm.id))
        finally:
            repo.close()
        return []

    @staticmethod
    def GetAllMembers() -> List[ViewMember]:
        repo = MemberRepo()
        try:
            members = repo.selectall_members()
        finally:
            repo.close()
        return [
            ViewMember(
                name=m.member_name,
                id=str(m.member_id),
                contact=m.member_contact,
                type=m.member_type,
            ) for m in members
        ]

    @staticmethod
    def UpdateMember(vm: ViewMember) -> List[str]:
        errs = ManageMember._validate(vm)
        if not vm.id.strip():
            errs.append("Member ID is required to update.")
        if errs:
            return errs
        updated = Member(
            member_name=vm.name.strip(),
            member_id=int(vm.id),
            member_contact=vm.contact.strip(),
            member_type=vm.type.strip(),
        )
        repo = MemberRepo()
        try:
            repo.update_member(updated)
        finally:
            repo.close()
        return []

    @staticmethod
    def DeleteMember(vm: ViewMember) -> List[str]:
        if not vm.id.strip() or not vm.id.isdigit():
            return ["Valid Member ID is required to delete."]
        repo = MemberRepo()
        try:
            repo.delete_member(int(vm.id))
        finally:
            repo.close()
        return []
