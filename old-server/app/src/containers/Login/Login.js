import React from 'react';
import PropTypes from 'prop-types';
import { Route, Switch } from 'react-router-dom';
import RequestOTP from 'components/RequestOTP';
// import VerifyOTP from 'components/VerifyOTP';
// import { requestOTPAPI, verifyOTPAPI } from 'api/auth';
import { loginCallbackAPI } from 'api/auth';
import Config from 'config';
import './Login.scss';

class Login extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      // phoneNumber: '',
      // email: '',
      // otp: '',
      // isCtaDisabled: true,
      errorMessage: '',
    };
  }

  componentDidMount() {
    console.log('Test');
    // const phoneNumber = sessionStorage.getItem('phoneNumber');
    // if (phoneNumber) {
    //   this.setState({
    //     phoneNumber,
    //   }, this.checkCtaDisabled);
    // }
    window.gapi.load('auth2', () => {
      window.gapi.auth2.init({
        client_id: Config.GOOGLE_CLIENT_ID,
      }).then((authResponse) => {
        const auth = authResponse;
        window.gapi.signin2.render('my-signIn', {
          scope: 'https://www.googleapis.com/auth/plus.login',
          longtitle: false,
          width: 150,
          height: 50,
          theme: 'light',
          onsuccess: this.onSignIn,
          onfailure: this.onFailure,
        });
        auth.isSignedIn.listen(this.signinChanged);
      });
    });
  }

  // handleRequestOTPInput = (e) => {
  //   const { name, value } = e.target;
  //   if (name === 'phoneNumber' && value && !/^[\d]{0,10}$/.test(value)) {
  //     return;
  //   }
  //   this.setState({
  //     [name]: value,
  //     errorMessage: '',
  //   }, this.checkCtaDisabled);
  // }

  // handleVerifyOTPInput = (e) => {
  //   const { value } = e.target;
  //   if (value && !/^[\d]{0,4}$/.test(value)) {
  //     return;
  //   }
  //   this.setState({
  //     otp: value,
  //     errorMessage: '',
  //   }, this.checkCtaDisabled);
  // }

  // handleCtaNext = () => {
  //   const { phoneNumber, otp } = this.state;
  //   const { location: { pathname }, history } = this.props;
  //   if (/verify/.test(pathname)) {
  //     verifyOTPAPI(phoneNumber, otp)
  //       .then((response) => {
  //         if (response.status === 200) {
  //           console.log('Verification successful!');
  //           sessionStorage.removeItem('phoneNumber');
  //           this.setState({
  //             phoneNumber: '',
  //             otp: '',
  //             email: '',
  //           });
  //           history
  //           .replace(`/app/login/success?authToken=${response.data.token}&phone=${phoneNumber}`);
  //         } else {
  //           this.setState({
  //             errorMessage: response.data.error,
  //           });
  //         }
  //       });
  //   } else {
  //     requestOTPAPI(phoneNumber)
  //       .then((response) => {
  //         if (response.status === 200) {
  //           console.log('Otp sent!');
  //           sessionStorage.setItem('phoneNumber', phoneNumber);
  //           history.push('/app/login/verify');
  //           this.checkCtaDisabled();
  //         } else {
  //           this.setState({
  //             errorMessage: response.data.error,
  //           });
  //         }
  //       });
  //   }
  // }

  // checkCtaDisabled = () => {
  //   const { phoneNumber, otp } = this.state;
  //   const { location: { pathname } } = this.props;
  //   let flag = true;
  //   if (/verify/.test(pathname)) {
  //     if (otp.length === 4) {
  //       flag = false;
  //     }
  //   } else if (phoneNumber.length === 10) {
  //     flag = false;
  //   } else {
  //     flag = true;
  //   }
  //   this.setState({
  //     isCtaDisabled: flag,
  //   });
  // }

  signinChanged = (signedIn) => {
    console.log('Signin state changed to ', signedIn);
    const container = document.getElementsByClassName('abcRioButtonContents')[0];
    if (signedIn) {
      container.children[0].style.display = 'none';
      container.children[1].style.display = '';
    } else {
      container.children[0].style.display = '';
      container.children[1].style.display = 'none';
    }
  }

  onSignIn = (googleUser) => {
    const { history } = this.props;
    // const profile = googleUser.getBasicProfile();
    // console.log(`ID: ${profile.getId()}`);
    // console.log(`Name: ${profile.getName()}`);
    // console.log(`Image URL: ${profile.getImageUrl()}`);
    // console.log(`Email: ${profile.getEmail()}`);
    // console.log('Client id token: ', googleUser.getAuthResponse().id_token);
    const idToken = googleUser.getAuthResponse().id_token;
    const email = googleUser.getBasicProfile().getEmail();
    loginCallbackAPI(idToken, email)
      .then((response) => {
        if (response.status === 200) {
          history.push(`/app/login/success?authToken=${idToken}`);
        }
      });
  }

  render() {
    const {
      // phoneNumber, email, otp, isCtaDisabled,
      errorMessage,
    } = this.state;
    // const { location: { pathname } } = this.props;
    return (
      <div className="login">
        <Switch>
          <Route exact path="/app/login">
            <RequestOTP />
          </Route>
          {/* <Route path="/app/login/verify">
            <VerifyOTP
              phoneNumber={phoneNumber}
              otp={otp}
              handleVerifyOTPInput={this.handleVerifyOTPInput}
            />
          </Route> */}
          <Route path="/app/login/success">
            <div>Login Success!</div>
          </Route>
        </Switch>
        {errorMessage
          ? <div className="login__error">{errorMessage}</div>
          : ''}
        {/* pathname !== '/app/login/success'
          ? (
            <div className="login__cta">
              <button type="button" onClick={this.handleCtaNext}
                disabled={isCtaDisabled}>Next</button>
            </div>
          )
          : '' */}
      </div>
    );
  }
}

Login.propTypes = {
  location: PropTypes.shape({
    pathname: PropTypes.string.isRequired,
  }).isRequired,
  history: PropTypes.shape({
    push: PropTypes.func.isRequired,
    replace: PropTypes.func.isRequired,
  }).isRequired,
};

export default Login;
