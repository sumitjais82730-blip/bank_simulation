import gmail

def send_credentials(email,name,acn,pwd):
    con=gmail.GMail('#your gamil','#app passowrd')
    body=f'''Welcome {name},
    Welcome to SumJaiz Bank.
    Here is your account details
    Account No. = {acn}
    Password = {pwd}

    Kindly change your password when you login first time.
    Thank You for opening account.

    SumJaiz Bank
    Bareilly (U.P.)

'''
    msg=gmail.Message(to=email,subject='Your cedentials for operating account.',text=body)
    con.send(msg)


def send_otp(email,name,otp):
    con=gmail.GMail('#your gamil','#app passowrd')
    body=f'''Hello {name},
    Here is your otp for your password
    OTP = {otp}
    Please verify your account.
    If you didn't send this otp.Don't share to anyone.
    Please contact with SumJaiz Bank.

    SumJaiz Bank
    Bareilly (U.P.)

'''
    msg=gmail.Message(to=email,subject='Your OTP for password.',text=body)
    con.send(msg)


def send_withdraw_otp(email,name,otp,amt):
    con=gmail.GMail('#your gamil','#app passowrd')
    body=f'''Hello {name},
    Here is your otp for withdraw {amt}
    OTP = {otp}
    Please enter OTP for withdraw.
    If you didn't send this otp.Don't share to anyone.
    Please contact with SumJaiz Bank.

    SumJaiz Bank
    Bareilly (U.P.)

'''
    msg=gmail.Message(to=email,subject='Your OTP for withdraw',text=body)
    con.send(msg)


def send_transfer_otp(email,name,otp,amt,to_acn):
    con=gmail.GMail('#your gamil','#app passowrd')
    body=f'''Hello {name},
    Here is your otp for transfer {amt} to ACN : {to_acn}
    OTP = {otp}
    Please enter OTP for transfer.
    If you didn't send this otp.Don't share to anyone.
    Please contact with SumJaiz Bank.

    SumJaiz Bank
    Bareilly (U.P.)

'''
    msg=gmail.Message(to=email,subject='Your OTP for trf.',text=body)

    con.send(msg)
