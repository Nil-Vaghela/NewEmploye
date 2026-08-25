import pandas as pd

class EmployeIDList:
    def __init__(self) -> None:
        pass

    def names_to_user_ids(names):
        user_ids = {}
        user_id_start = 101
        for i, name in enumerate(names):
            first_name, last_name = name.split(" ")
            new_name = f"{first_name} {last_name[0]}."
            user_ids[new_name] = user_id_start + i
        return user_ids

    names_list = ["Nil Vaghela", 
                "Joshua Coleman", 
                "Khalin Wallace",
                "Ja'Bree Johnson",
                "Milaan Williams",
                "Jalil Coast",
                "Cecilia Keown",
                "Taisa Bethal",
                "Viviana Torres",
                "Sania Robinson",
                "Mukhil Bhaskaran",
                "Rahul kanwar",
                "Joseph Singoy",
                "Khayri Moore",
                "Kimone Robinson",
                "Milaan Williams",
                "Milagros Barreto",
                "Morgan Moye",
                "Shaniel Walters",
                "Shereece Bhagwandass",
                "Tiya Davis",
                "Vaughn Ambrus",
                "Vincent Googe",
                "Noel Gilkes",
                "Oghenerume Edward",
                "Patricia Kamara",
                "Reine Ahountsa",
                "Roman Cowart",
                "Rylee Watson",
                "Ja'Mya Smith",
                "Jadyn Franklin",
                "James Ramsey",
                "Jayla Gordon",
                "John barnes",
                "Aniya Cheely",
                "Anjiya Macheswala",
                "Ava McClain",
                "Carlos Mejia",
                "Cayman Campbell",
                "Christopher Ramos",
                "Edward Larbi",
                "Golden Joeaneke",
                "A'maya Wilson",
                "Aaliyah Gille",
                "Alexander Nunez",
                "Alexis Johnson",
                ]

    users_data = names_to_user_ids(names_list)


    def save_users_data_to_excel(users_data, file_name="Employee Names.xlsx"):
        df = pd.DataFrame(users_data.items(), columns=["Name", "User ID"])
        df.to_excel(file_name, index=False)

    save_users_data_to_excel(users_data)
