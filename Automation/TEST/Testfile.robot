*** Settings ***
Library                ../GUI/Autofuntion.py

*** Variables ***
${url}        http://localhost:4200/account/login        
${name_product}             HADES STRIPED SOLID SHIRT   
${quantity}                   2                             
${user_name}            phong tran 123     
${number}                0999999999        #(10 chữ số)
${mail}                phongtran@gmail.com        
${address}            11 au co                     
${province}            An Giang        
${district}            Châu Đốc        
${ward}                Châu Phú A        

${price}               894000        # phụ thuộc giá tiền sản phẩm * số lượng * giảm giá 

# vd: với sản phẩm name:ABYSS SS24 STARRY PINK TEE -> mua với quantity = 2 -> ${price}=   980000đ (490000đ * 2 + 0đ phí vận chuyển )

*** Test Cases ***    
Open Browser Example
    launch_browser    ${url}
    login        user@example.com        123456789
    add_products_to_cart        ${name_product}        ${quantity}
    fill_checkout_form           ${user_name}       ${mail}        ${number}    ${address}     ${province}    ${district}         ${ward}
    verify_order_in_my_account    ${user_name}        ${number}       ${address}          ${ward}       ${district}        ${province}      ${price}
    Close Browser   
