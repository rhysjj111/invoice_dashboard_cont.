def registration_normalize(self):
    reg = self.registration.replace(" ", "").upper()
    if len(reg) > 3:
        reg_list = list(reg)
        reg_list.insert(-3, " ")
        reg = "".join(reg_list)
    self.registration = reg
    return self.registration

def name_normalize(self):
    self.name = " ".join(self.name.split()).title()
    return self.name