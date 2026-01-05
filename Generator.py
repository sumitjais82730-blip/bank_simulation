import random
def generate_pass():
    pwd=''
    for i in range(2):
        c=chr(random.randint(97,122))
        pwd+=c

        c=chr(random.randint(65,90))
        pwd+=c

        c=chr(random.randint(97,122))
        pwd+=c

    return pwd

#print(generate_pass())

def gen_otp():
    otp=random.randint(1000,9999)
    return otp

#print(gen_otp())