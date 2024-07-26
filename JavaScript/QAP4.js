/* Description: Program for a Motel to store and view customer data.
Author: Sarah Murphy
Date: July 19, 2024 */

const customer = {
    name: "Sarah Murphy",
    birthdate: new Date ("1997-11-10T00:00:00"),
    gender: "female",
    roomprefs: ["top floor", "king sized bed", "near elevator", "garden view"],
    paymethod: "credit card",
    mailaddress: {
        street: "101 Duckworth Street",
        city: "St. John's",
        province: "NL",
        postcode: "A1A 1A1",
        country: "Canada",
    },
    phonenum: "(709) 555-0123",
    staydates: {
        checkin: new Date("2024-07-10T00:00:00"),
        checkout: new Date ("2024-07-15T00:00:00"),
    },

    age_calc: function() {
        this.today = new Date()
        let ageMilli = this.today - this.birthdate // Converting to milliseconds.
        return Math.floor(ageMilli / 31556952000) // Converting milliseconds to years.
        },
        
    stay_duration: function() {
        let stay_durationMilli = this.staydates.checkout - this.staydates.checkin // Converting to milliseconds.
        return Math.floor(stay_durationMilli / 86400000) // Converting from milliseconds to days.
        },

};

let description = `The customer's name is ${customer.name}, a ${customer.age_calc()} year old ${customer.gender} client whose birthdate is ${customer.birthdate.getFullYear()}-${customer.birthdate.getMonth()+1}-${customer.birthdate.getDate()}. This customer will be staying at our motel for ${customer.stay_duration()} days, from ${customer.staydates.checkin} until ${customer.staydates.checkout}. Please ensure they receive a room to their liking, which includes ${customer.roomprefs.join(", ")}. They will be paying with ${customer.paymethod} upon check-out. To contact this client, please use the following phone number: ${customer.phonenum}. Please see the following mailing address to ensure their invoice gets delivered to the right location:
        ${customer.mailaddress.street},
        ${customer.mailaddress.city}, ${customer.mailaddress.province}
        ${customer.mailaddress.country}
        ${customer.mailaddress.postcode}.
        Thank you.`;

console.log(description)

document.getElementById("scriptcontent").innerHTML = description
