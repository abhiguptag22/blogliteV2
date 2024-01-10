<template>
    <div class="container-fluid">
        <div class="login-box">
            <div class="row">
                <div class="col-5">
                    <img src="../assets/img/logo.png" class="logo" alt="">
                </div>
                <div class="col-7">
                    <div class="login-heading">
                        <h3>Log in</h3>
                    </div>
                    <div class="login-form">
                        <input type="email" placeholder="Enter your email-address" v-model="email">
                        <br><br>
                        <input type="password" placeholder="Enter your password" v-model="password">
                        <br><br>
                        <b-button id="login-btn" @click="loginHandle">Log in</b-button>
                        <br><br>
                        <p v-if="notvalid" class="red"> &#x2022; Please input valid details.</p>
                        <p v-if="wrongPass" class="red"> &#x2022; Email and password combination does not match.</p>
                        <br><br>
                        <p class="create-btn" @click="handleCreateLink">Create a New Account</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default  {
    name: 'Login_page',
    data : function() {
        return {
            email:null,
            password:null,
            notvalid:false,
            access_token:"",
            wrongPass:false
        }
    },
    methods : {
        async loginHandle() {
            if (this.email==null || this.password == null) {
                this.notvalid=true
            }
            else {
            const loginRequest = await fetch("http://localhost:5000/logins", {
                method:'POST',
                body: JSON.stringify({
                        email: this.email,
                        password: this.password
                        }),
                headers: {
                "Content-type": "application/json; charset-UTF-8",
                }
            })
        
            const jResponse = await loginRequest.json()

            if (jResponse.token) {
                localStorage.setItem('token', jResponse.token)
                console.log(jResponse.token)
                document.body.style.backgroundColor = '#f2f2f2'
                this.$router.push({name:'home'})
            }
            else {
                this.notvalid=false
                this.wrongPass=true
            }

            }
        },
        handleCreateLink() {
            this.$router.push({name:'sign_up'})
        }
    },
    mounted: function() {
            console.log("here")
            document.body.style.backgroundColor = '#000038'
            
            localStorage.removeItem("taskId")
        }
}
</script>

<style>
.login-box {
    width:700px;
    height: 450px;
    margin-top: 100px;
    background-color: white;
    margin-left: auto;
    margin-right: auto;
    border-radius: 15px;
}
.col-7 {
    height: 450px;
    border-left: 3px solid gray;
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
    margin-top: 70px;

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
.create-btn {
    color: rgb(104, 102, 102);
}
</style>