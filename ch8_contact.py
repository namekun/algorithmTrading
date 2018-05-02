#-*- coding: utf-8 -*-


class Contact:
    def __init__(self, name, phone_number, e_mail, addr):
        self.name = name
        self.phone_number = phone_number
        self.e_mail = e_mail
        self.addr = addr

    def print_info(self):
        print("Name :", self.name)
        print("Phone Number:", self.phone_number)
        print("E-Mail :", self.e_mail)
        print("Address :", self.addr)


def print_menu():
    print("1. 연락처 입력")
    print("2. 연락처 출력")
    print("3. 연락처 삭제")
    print("4. 연락처 저장")
    print("5. 종료")
    menu = input("메뉴 선택 :")
    return int(menu)


def set_contact():
    name = input("Name :")
    phone_number = input("Phone Number :")
    e_mail = input("E-Mail :")
    addr = input("Address :")

    contact = Contact(name, phone_number, e_mail, addr)
    return contact


def print_contact(contact_list):
    print()
    for contact in contact_list:
        contact.print_info()
    print()


def delete_contact(contact_list, name):
    for i, contact in enumerate(contact_list):
        if contact.name == name:
            del contact_list[i]


def store_contact(contact_list):
    f = open("contact_db.txt", "wt")  # wt = write text 모드 로 파일을 열어라.
    for contact in contact_list:
        f.write(contact.name + '\n')
        f.write(contact.phone_number + '\n')
        f.write(contact.e_mail + '\n')
        f.write(contact.addr + '\n')
    f.close()


def load_contact(contact_list):
    f = open("contact_db.txt", "rt", encoding='UTF8')
    lines = f.readlines()
    num = len(lines) / 4
    num = int(num)

    for i in range(num):
        name = lines[4 * i].rstrip('\n')
        phone_number = lines[4 * i + 1].rstrip('\n')
        email = lines[4 * i + 2].rstrip('\n')
        addr = lines[4 * i + 3].rstrip('\n')
        contact = Contact(name, phone_number, email, addr)
        contact_list.append(contact)
    f.close()


def run():
    contact_list = []
    load_contact(contact_list)
    while 1:
        menu = print_menu()
        if menu == 1:
            contact = set_contact()
            contact_list.append(contact)
        elif menu == 2:
            print_contact(contact_list)
        elif menu == 3:
            name = input("Name :")
            if name in contact_list:
                delete_contact(contact_list, name)
            else:
                print("없는 이름입니다.")
        elif menu == 4:
            store_contact(contact_list)
        elif menu == 5:
            break
        else:
            print("Error! 없는 메뉴 입니다.")


if __name__ == "__main__":
    run()



