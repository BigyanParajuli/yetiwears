const express = require('express');
const bodyParser = require('body-parser');
const nodemailer = require('nodemailer');

const app = express();
app.use(bodyParser.urlencoded({ extended: true }));

// Configure your SMTP settings
const transporter = nodemailer.createTransport({
    service: 'gmail', // Example using Gmail; use your SMTP provider
    auth: {
        user: 'yourEmail@gmail.com',
        pass: 'yourEmailPassword'
    }
});

app.post('/forgot-password', (req, res) => {
    const { email } = req.body;
    // Here, implement logic to generate an OTP and store it in your database with a timestamp
    const otp = Math.floor(100000 + Math.random() * 900000); // Example 6-digit OTP
    console.log(`Generated OTP for ${email}: ${otp}`);
    // Save OTP to database with expiration time (not shown)

    const mailOptions = {
        from: 'yourEmail@gmail.com',
        to: email,
        subject: 'Reset your password',
        text: `Your OTP is ${otp}. It is valid for 10 minutes.`
    };

    transporter.sendMail(mailOptions, (error, info) => {
        if (error) {
            console.log(error);
            res.send('Error sending email');
        } else {
            console.log('Email sent: ' + info.response);
            res.send('OTP sent to your email');
        }
    });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
