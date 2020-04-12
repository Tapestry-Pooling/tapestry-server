import React from 'react';
import PropTypes from 'prop-types';
import { Route, Switch } from 'react-router-dom';
import RequestOTP from 'components/RequestOTP';
import VerifyOTP from 'components/VerifyOTP';
import { requestOTPAPI, verifyOTPAPI } from 'api/auth';
import './Login.scss';

class Login extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      phoneNumber: '',
      email: '',
      otp: '',
      isCtaDisabled: true,
      errorMessage: '',
    };
  }

  componentDidMount() {
    console.log('Test');
    const phoneNumber = sessionStorage.getItem('phoneNumber');
    if (phoneNumber) {
      this.setState({
        phoneNumber,
      }, this.checkCtaDisabled);
    }
  }

  handleRequestOTPInput = (e) => {
    const { name, value } = e.target;
    if (name === 'phoneNumber' && value && !/^[\d]{0,10}$/.test(value)) {
      return;
    }
    this.setState({
      [name]: value,
      errorMessage: '',
    }, this.checkCtaDisabled);
  }

  handleVerifyOTPInput = (e) => {
    const { value } = e.target;
    if (value && !/^[\d]{0,4}$/.test(value)) {
      return;
    }
    this.setState({
      otp: value,
      errorMessage: '',
    }, this.checkCtaDisabled);
  }

  handleCtaNext = () => {
    const { phoneNumber, otp } = this.state;
    const { location: { pathname }, history } = this.props;
    if (/verify/.test(pathname)) {
      verifyOTPAPI(phoneNumber, otp)
        .then((response) => {
          if (response.status === 200) {
            console.log('Verification successful!');
            sessionStorage.removeItem('phoneNumber');
            this.setState({
              phoneNumber: '',
              otp: '',
              email: '',
            });
            history.replace(`/app/login/success?authToken=${response.data.token}`);
          } else {
            this.setState({
              errorMessage: response.data.error,
            });
          }
        });
    } else {
      requestOTPAPI(phoneNumber)
        .then((response) => {
          if (response.status === 200) {
            console.log('Otp sent!');
            sessionStorage.setItem('phoneNumber', phoneNumber);
            history.push('/app/login/verify');
            this.checkCtaDisabled();
          } else {
            this.setState({
              errorMessage: response.data.error,
            });
          }
        });
    }
  }

  checkCtaDisabled = () => {
    const { phoneNumber, otp } = this.state;
    const { location: { pathname } } = this.props;
    let flag = true;
    if (/verify/.test(pathname)) {
      if (otp.length === 4) {
        flag = false;
      }
    } else if (phoneNumber.length === 10) {
      flag = false;
    } else {
      flag = true;
    }
    this.setState({
      isCtaDisabled: flag,
    });
  }

  render() {
    const {
      phoneNumber, email, otp, isCtaDisabled,
      errorMessage,
    } = this.state;
    const { location: { pathname } } = this.props;
    return (
      <div className="login">
        <Switch>
          <Route exact path="/app/login">
            <RequestOTP
              phoneNumber={phoneNumber}
              email={email}
              handleRequestOTPInput={this.handleRequestOTPInput}
            />
          </Route>
          <Route path="/app/login/verify">
            <VerifyOTP
              phoneNumber={phoneNumber}
              otp={otp}
              handleVerifyOTPInput={this.handleVerifyOTPInput}
            />
          </Route>
          <Route path="/app/login/success">
            <div>Login Success!</div>
          </Route>
        </Switch>
        {errorMessage
          ? <div className="login__error">{errorMessage}</div>
          : ''}
        {pathname !== '/app/login/success'
          ? (
            <div className="login__cta">
              <button type="button" onClick={this.handleCtaNext} disabled={isCtaDisabled}>Next</button>
            </div>
          )
          : ''}
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
