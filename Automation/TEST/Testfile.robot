*** Settings ***
Library                ../GUI/Autofuntion.py

*** Variables ***
${url}        http://localhost:4200/account/login        #  chỗ này nhét link URL mình muốn làm việc với nó
${name_product}             HADES STRIPED SOLID SHIRT   # tên sản phẩm cho nó chạy click vô mua hàng, tên sản phẩm khác cũng đc, nhưng phải vào DB kiểm tr thêm sản phẩm để mua
${quantity}                   2                             # mua sản phẩm trên mấy cái, số khác vẫn đc -> nhưng đổi thì tính lại giá tiền + discount các thứ -> để nhét lại chỗ biến ${price} cho đúng
${user_name}            phong tran 123     #        tên người mua, muốn để tên gì cũng đc
${number}                0999999999        # sdt người mua, muốn để tên gì cũng đc (10 chữ số)
${mail}                phongtran@gmail.com        # mail người mua, muốn để tên gì cũng đc
${address}            hcm city                     #   địa chỉ, chỗ này viết sao cũng đc
${province}            An Giang        #  này phải chọn theo danh sách các tỉnh mới đc (hồ chí minh, hà nội, ...)
${district}            Châu Đốc        # phải chọn quận tương ứng với tỉnh ở trên (click province -> ròi mới chọn district đc)
${ward}                Châu Phú A        # phải chọn xã tương ứng với quận, tỉnh ở trên (click province -> ròi mới chọn district đc -> rồi mới chọn được ward)
# -> 3 cái này thì f12 xem option của từng cái, miễn có là chạy đc
${price}               894000        # phụ thuộc giá tiền sản phẩm * số lượng * giảm giá là ra được con số để điền chỗ này 

# vd: với sản phẩm name:ABYSS SS24 STARRY PINK TEE -> mua với quantity = 2 -> ${price}=   980000đ (490000đ * 2 + 0đ phí vận chuyển )

*** Test Cases ***    
Open Browser Example
    launch_browser    ${url}
    login        user@example.com        123456789
    add_products_to_cart        ${name_product}        ${quantity}
    fill_checkout_form           ${user_name}       ${mail}        ${number}    ${address}     ${province}    ${district}         ${ward}
    verify_order_in_my_account    ${user_name}        ${number}       ${address}          ${ward}       ${district}        ${province}      ${price}
    Close Browser   
    
    #  D:\Test\Automation\log.html -> để xem mình pass hay failed tại chỗ nào (đưa link này lên web là xem đc)