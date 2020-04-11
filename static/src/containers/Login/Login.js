import React from 'react';
import PropTypes from 'prop-types';
import { Route, Switch } from 'react-router-dom';
import RequestOTP from 'components/RequestOTP';
import { requestOTPAPI } from 'api/auth';
import './Login.scss';

class Login extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      phoneNumber: '',
      email: '',
    };
  }

  componentDidMount() {
    console.log('Test');
  }

  handleRequestOTPInput = (e) => {
    const { name, value } = e.target;
    if (name === 'phoneNumber' && value && !/^[\d]{0,10}$/.test(value)) {
      return;
    }
    this.setState({
      [e.target.name]: e.target.value,
    });
  }

  handleCtaNext = () => {
    const { phoneNumber } = this.state;
    const { location: { pathname } } = this.props;
    if (/verify/.test(pathname)) {
      // TODO: Do something
    } else {
      requestOTPAPI(phoneNumber)
        .then((response) => {
          if (response.status === 200) {
            console.log('Otp sent!');
          } else {
            console.log('show error!');
          }
        });
    }
  }

  render() {
    const { phoneNumber, email } = this.state;
    return (
      <div className="login">
        <Switch>
          <Route exact path="/login">
            <RequestOTP
              phoneNumber={phoneNumber}
              email={email}
              handleRequestOTPInput={this.handleRequestOTPInput}
            />
          </Route>
          <Route path="/login/verify">
            Verify OTP Component
          </Route>
        </Switch>
        <div className="login__cta">
          <button type="button" onClick={this.handleCtaNext}>Next</button>
        </div>
      </div>
    );
  }
}

Login.propTypes = {
  location: PropTypes.shape({
    pathname: PropTypes.string.isRequired,
  }).isRequired,
};

export default Login;
