def get_email_template_forgot_password(username, otp_code, endpoint_link):
    _nolanMLogoUrl = "https://drive.google.com/uc?id=1w3mfBR7NBooRlJWaQRmIcoNRbFROo32A"
    table_data = \
        f"""
        <!DOCTYPE html>
        <html>
            <head>
              <base target='_top'>
            </head>
            <body>
              <div style='font-family: Helvetica, Arial, sans-serif; min-width: 1000px; overflow: auto; line-height: 2'>
                <div style='margin: 50px auto; width: 80%; padding: 20px 0'>
                    <div style='border-bottom: 5px solid #eee'>
                        <a href='' style='font-size: 30px; color: #CC0000; text-decoration: none; font-weight: 600'>
                            Youtube Analysis Web Page - NolanM
                        </a>
                    </div>
                    <br>
                <p style='font-size: 22px'>Hello {username},</p>
                <p>Thank you for choosing our website and services. Please Use this OTP to complete your forgot password procedures and verify your request.</p>
                <p>Remember, Never share this OTP with anyone.</p><br><br>
                  <h2 style='margin: 0 auto; width: max-content; padding: 0 10px; color: #CC0000; border-radius: 4px;'>{otp_code}</h2><br>
                  <div style='text-align: center;'>
                  <a href='{endpoint_link}' style='background: #CC0000; color: #fff; text-decoration: none; padding: 2px 16px; border-radius: 10px; display: inline-block;'>Verify OTP</a><br><br></div><br>
                  <p style='font-size: 15px;'>Regards,<br /><br>NolanM</p>
                  <hr style='border: none; border-top: 5px solid #eee' />
                  <div style='float: left; padding: 8px 0; color: #aaa; font-size: 0.8em; line-height: 1; font-weight: 300'>
                   <img src='{_nolanMLogoUrl}' alt='NolanM Logo' style='width: 50%; max-height: 108px;'>
                </div>
                </div>
              </div>
            </body>
        </html>
                    """
    return table_data
