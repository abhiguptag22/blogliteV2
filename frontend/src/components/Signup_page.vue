<template>
    <div class="container-fluid">
        <div class="signup-box">
            <div class="row">
                <div class="col-5">
                    <img src="../assets/img/logo.png" class="logo" alt="">
                </div>
                <div class="col-7">
                    <div class="login-heading">
                        <h3>Create a New Account</h3>
                    </div>
                    <div class="login-form">
                        <input type="text" placeholder="Type your full name" v-model="fullname">
                        <p v-if="nameNemail" class="red">Please enter your name.</p>
                        <div v-else style="max-height: 20px;"><br><br></div>
                        <input type="email" placeholder="Enter your email-address" v-model="email">
                        <p v-if="nameNemail" class="red">Please enter your email address.</p>
                        <div v-else style="max-height: 20px;"><br><br></div>
                        <input type="password" placeholder="Create a new password" v-model="password">
                        <p v-if="passwordlength" class="red">Password should be of at least 7 characters.</p>
                        <div v-else style="max-height: 20px;"><br><br></div>
                        <input type="password" placeholder="Re-enter your new password" v-model="repassword">
                        <p v-if="passwordmatch" class="red">Both passwords should match exactly.</p>
                        <div v-else style="max-height: 20px;"><br><br></div>
                        <b-button id="login-btn" @click="signupHandle">Sign Up</b-button>
                        <br><br>
                        <p class="create-btn" @click="handleLoginLink">Already Have an Account? Log in</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default  {
    name: 'Signup_page',
    data : function() {
        return {
            fullname: null,
            email:null,
            password:null,
            repassword:null,
            passwordlength:false,
            passwordmatch:false,
            nameNemail:false
        }
    },
    methods : {
        async signupHandle() {
            if (this.fullname == null || this.email == null || this.password == null || this.repassword == null) {
                console.log(1)
                this.nameNemail=true
                this.passwordlength=true
                this.passwordmatch=true
            }
            else if (this.password.length < 7) {
                console.log(2)
                this.passwordlength = true
            }
            else if (this.password!==this.repassword) {
                this.passwordmatch=true
            }
            else {
            const regRequest = await fetch(`http://localhost:5000/signup`, {
            method: "POST",
            body: JSON.stringify({
               name:this.fullname,
               email: this.email,
               password: this.password
            }),
            headers: {
               "Content-type": "application/json; charset-UTF-8"
            }
            })
            const message = await regRequest.json()
            console.log(message)
            if (message.msg=="Registration successful") {
                console.log('here')
                this.$router.push({name:'login'})
            }
        }
        },
        handleLoginLink() {
            this.$router.push({name:'login'})
        }
    },
    mounted: function() {
            console.log("here in signyp")
            document.body.style.backgroundColor = '#000038'
        }
}
</script>

<style>
.signup-box {
    width:700px;
    height: 470px;
    margin-top: 100px;
    background-color: white;
    margin-left: auto;
    margin-right: auto;
    border-radius: 15px;
}
.col-7 {
    height: 470px;
    border-left: 3px solid #000038;
}
.logo {
    margin-top: 170px;
    margin-left: 15px;
    height: 125px;
    width: auto;
}
.login-heading {
    margin-top: 40px;
}
.login-form {
    margin-top: 20px;

}
.login-form input {
    border-top-style: hidden;
    border-left-style: hidden;
    border-right-style: hidden;
    border-bottom-style: groove;
    background-color: #f3f3f3;
    width: 300px;
    height: 45px;

}
input:focus {
    outline: none;
}
#login-btn {
    background-color: #000038;
}
.red {
    font-size: 0.8rem;
    color: red;
    text-align: left;
    margin: auto;
    width: 300px;
}
.create-btn {
    color: rgb(104, 102, 102);
}
</style>