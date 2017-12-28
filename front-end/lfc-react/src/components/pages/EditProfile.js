import React from "react";
import PropTypes from "prop-types";
import decode from "jwt-decode";
import axios from "axios";
import {Button} from "semantic-ui-react";
import setAuthorizationHeader from "../../utils/setAuthorizationHeader";

let theToken = localStorage.lfcJWT;


class EditProfile extends React.Component {
    constructor() {
        super();
        this.state = {
            user: {
                username: '',
                email: '',
                first_name: '',
                last_name: '',
                birth_date: '',
            },
        };
        this.handleFirstName = this.handleFirstName.bind(this);
        this.handleLastName = this.handleLastName.bind(this);
        this.handleEmail = this.handleEmail.bind(this);
        this.handleBirthDate = this.handleBirthDate.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }




    handleFirstName(event) {
        this.setState({
            first_name: event.target.value,
        });
    }

    handleLastName(event) {
        this.setState({
            last_name: event.target.value,
        });
    }

    handleEmail(event) {
        this.setState({
            email: event.target.value,
        });
    }

    handleBirthDate(event) {
        this.setState({
            birth_date: event.target.value,
        });
    }

    handleSubmit(event) {
        setAuthorizationHeader(theToken);
        axios.put('http://34.210.127.92:8000/user/edit_profile/', {
            'first_name': this.state.first_name,
            'last_name': this.state.last_name,
            'email': this.state.email,
            'birth_date' : this.state.birth_date,
        }, {
            'Content-Type': 'application/json',
        }).then(response => {
            const payload = decode(theToken);
            const user_id = payload.user_id;
           window.location.assign('/me');
        }, error => {
            console.log("error");
        });
        event.preventDefault();
    }

  render() {
        return (
            <form className="ui form" id="editProfile" onSubmit={this.handleSubmit}>
                <div className=" field">
                    <h1>Edit Profile Form</h1>
                    First Name :<input type="text"  placeholder={this.state.user.first_name}
                           onChange={this.handleFirstName}/> <br/>
                    Last Name:
                    <input type="text" placeholder={this.state.user.last_name}
                           onChange={this.handleLastName}/> <br/>
                    Email:
                    <input type="text" placeholder={this.state.user.email}
                           onChange={this.handleEmail}/> <br/>
                    Birth-Date
                    <input type="date" placeholder={this.state.user.birth_date}
                           onChange={this.handleBirthDate}/> <br/>
                    <br/>
                    <Button type="submit"> Edit </Button>
                </div>
            </form>




        );
    }


}

EditProfile.propTypes = {
    isAuthenticated: PropTypes.bool.isRequired
};

function mapStateToProps(state) {
    return {
        isAuthenticated: !!state.user.accessToken
    };
}

export default EditProfile;

