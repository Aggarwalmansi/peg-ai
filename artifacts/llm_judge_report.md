# LLM-as-Judge Evaluation

### `delivery_hinglish_scam_001`
- **Input:** Sir maine aapko OTP bheja hai delivery confirm karne ke liye, kripya share kare taaki order deliver ho sake
- **Label:** scam
- **Reasoning:** The message asks you to 'share' an OTP, which is a red flag for phishing scams.
- **Judge Verdict:** grounded
- **Judge Explanation:** The reasoning correctly identifies the request to 'share' an OTP as a red flag for phishing scams, as it is a common tactic used by scammers to trick users into revealing sensitive information.

### `delivery_safe_001`
- **Input:** Your Amazon delivery agent is at the gate. Share OTP to receive your order.
- **Label:** scam
- **Reasoning:** The message asks to share OTP with a stranger, which is a common tactic used by scammers to trick victims into revealing sensitive information.
- **Judge Verdict:** grounded
- **Judge Explanation:** The reasoning correctly identifies the intent behind the message as a scam, as it asks the recipient to share sensitive information with a stranger.

### `upi_scam_003`
- **Input:** Your refund of Rs.1500 has been initiated. Scan this QR code and enter UPI pin to receive the money in your account.
- **Label:** scam
- **Reasoning:** The message asks to 'Scan this QR code and enter UPI pin' which is a suspicious request for a refund, indicating a potential phishing attempt.
- **Judge Verdict:** grounded
- **Judge Explanation:** The reasoning correctly identifies the suspicious request for a UPI pin as a potential phishing attempt, indicating a grounded understanding of the context and intent.

### `otp_scam_004`
- **Input:** Your mobile number will be deactivated in 2 hours. Call customer care at 9876543210 and share your OTP to continue service.
- **Label:** scam
- **Reasoning:** The message demands sharing of OTP to continue service, which is a red flag for a scam.
- **Judge Verdict:** grounded
- **Judge Explanation:** The reasoning correctly identifies the demand for sharing OTP as a red flag for a scam, indicating a grounded understanding of the intent and context.

### `bank_safe_005`
- **Input:** Is this the right link for the Income Tax portal? eportal.incometax.gov.in
- **Label:** safe
- **Reasoning:** The message is asking for verification of a legitimate government portal link, indicating a normal discussion.
- **Judge Verdict:** grounded
- **Judge Explanation:** The AI correctly identifies the intent as verification of a legitimate government portal link, demonstrating a grounded understanding of the context.

### `bank_safe_001`
- **Input:** I'm going to the bank today to update my KYC documents.
- **Label:** safe
- **Reasoning:** The message mentions a normal, routine bank visit to update KYC documents, which is a legitimate activity.
- **Judge Verdict:** grounded
- **Judge Explanation:** The reasoning correctly identifies the context and intent of the message as a routine bank visit, which is a legitimate activity.

### `bank_scam_005`
- **Input:** This is Rahul from your bank's fraud prevention team. We noticed suspicious activity. Can you confirm the last 4 digits of your card so I can secure your account?
- **Label:** scam
- **Reasoning:** The message asks to confirm the last 4 digits of your card, which is a suspicious request that could be an attempt to extract sensitive information.
- **Judge Verdict:** grounded
- **Judge Explanation:** The reasoning correctly identifies the suspicious request for card information as a potential scam, demonstrating an understanding of the context and intent.

