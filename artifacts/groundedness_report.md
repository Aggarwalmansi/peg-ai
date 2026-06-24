# Phase 2 Groundedness Eval

### `delivery_hinglish_scam_001`
- **Input:** Sir maine aapko OTP bheja hai delivery confirm karne ke liye, kripya share kare taaki order deliver ho sake
- **Label:** scam
- **Reasoning:** The message asks you to 'share' an OTP, which is a red flag for phishing scams.
- **Grounded:** False

### `delivery_safe_001`
- **Input:** Your Amazon delivery agent is at the gate. Share OTP to receive your order.
- **Label:** scam
- **Reasoning:** The message asks to 'Share OTP' to receive an order, which is a suspicious request for sensitive information.
- **Grounded:** True

### `upi_scam_003`
- **Input:** Your refund of Rs.1500 has been initiated. Scan this QR code and enter UPI pin to receive the money in your account.
- **Label:** scam
- **Reasoning:** The message asks to 'Scan this QR code and enter UPI pin' which is a suspicious request for a refund, indicating a potential phishing attempt.
- **Grounded:** True

### `otp_scam_004`
- **Input:** Your mobile number will be deactivated in 2 hours. Call customer care at 9876543210 and share your OTP to continue service.
- **Label:** scam
- **Reasoning:** The message demands sharing of OTP to continue service, which is a red flag for a scam.
- **Grounded:** True

### `bank_safe_005`
- **Input:** Is this the right link for the Income Tax portal? eportal.incometax.gov.in
- **Label:** safe
- **Reasoning:** The message asks about the legitimacy of a link, indicating a normal discussion or inquiry rather than a scam.
- **Grounded:** False

### `bank_safe_001`
- **Input:** I'm going to the bank today to update my KYC documents.
- **Label:** safe
- **Reasoning:** The message mentions a normal banking activity, 'update my KYC documents', which is a legitimate reason to visit the bank.
- **Grounded:** True

### `bank_scam_005`
- **Input:** This is Rahul from your bank's fraud prevention team. We noticed suspicious activity. Can you confirm the last 4 digits of your card so I can secure your account?
- **Label:** scam
- **Reasoning:** The message asks to confirm the last 4 digits of your card, which is a suspicious request that could be used to steal your card information.
- **Grounded:** True

### `upi_scam_006`
- **Input:** Your KYC for Paytm is pending. Send Re.1 via UPI to verify your bank account.
- **Label:** scam
- **Reasoning:** The message asks to send Re.1 via UPI to verify the bank account, which is a suspicious request that could be a scam.
- **Grounded:** True

### `upi_scam_002`
- **Input:** Hello I am from Olx. To receive payment for your furniture, open Google Pay and click 'Pay' to authorize my transaction.
- **Label:** scam
- **Reasoning:** The message asks you to click 'Pay' to authorize a transaction, which is a suspicious request that could be a phishing attempt.
- **Grounded:** True

### `clear_negative_001`
- **Input:** Hey, are we still meeting for lunch tomorrow at 1pm?
- **Label:** safe
- **Reasoning:** The message mentions a casual meeting invitation with no urgency or request for sensitive information, indicating a normal conversation.
- **Grounded:** False

### `otp_hinglish_safe_002`
- **Input:** Mera OTP nahi aaya, customer care ko call karna padega kya?
- **Label:** safe
- **Reasoning:** The message mentions 'OTP nahi aaya' which indicates a normal discussion about not receiving an OTP, rather than a scammer asking for OTP.
- **Grounded:** True

### `job_safe_004`
- **Input:** The interview is scheduled for tomorrow at 10 AM over Google Meet.
- **Label:** safe
- **Reasoning:** The message mentions a scheduled interview over Google Meet, which is a normal and legitimate activity, without any signs of urgency, pressure, or malicious intent.
- **Grounded:** True

