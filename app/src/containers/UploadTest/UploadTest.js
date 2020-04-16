import React from 'react';
import PropTypes from 'prop-types';
import { Route, Switch } from 'react-router-dom';
import {
  getDashboardDataAPI, getCellDataAPI,
  uploadTestDataAPI, getResultAPI,
} from 'api/test';
import UploadTestLandingPage from 'components/UploadTestLandingPage';
import UploadTestForm from 'components/UploadTestForm';
import UploadTestResult from 'components/UploadTestResult';
import './UploadTest.scss';

class UploadTest extends React.Component {
  constructor(props) {
    super(props);
    const urlParams = new URLSearchParams(window.location.search);
    this.state = {
      testId: '',
      testsData: [],
      cellData: [],
      result: '',
      authToken: urlParams.get('authToken') || sessionStorage.getItem('authToken'),
      phone: urlParams.get('phone') || sessionStorage.getItem('phone'),
      isCtaDisabled: true,
    };
  }

  componentDidMount() {
    const { authToken, phone } = this.state;
    const { location: { pathname } } = this.props;
    if (pathname === '/app/upload-test') {
      getDashboardDataAPI(authToken, phone)
        .then((response) => {
          console.log('response: ', response.data.data);
          sessionStorage.setItem('authToken', authToken);
          sessionStorage.setItem('phone', phone);
          sessionStorage.setItem('testsData', JSON.stringify(response.data.data));
          this.setState({
            testsData: response.data.data,
            cellData: [],
            result: '',
          });
        });
    } else if (pathname === '/app/upload-test/form') {
      const testsDataLocal = JSON.parse(sessionStorage.getItem('testsData'));
      const urlParams = new URLSearchParams(window.location.search);
      const testId = urlParams.get('testId');
      const testData = testsDataLocal.filter((data) => (data.test_id === parseInt(testId, 10)))[0];
      getCellDataAPI(authToken, testData.batch)
        .then((response) => {
          this.setState({
            cellData: response.data.cellData.map((label, index) => ({ label, isChecked: (testData.test_data === undefined || testData.test_data[index] === 100), value: testData.test_data ? testData.test_data[index].toString() : '100' })),
            testId,
            testsData: testsDataLocal,
          }, this.checkCtaDisabled);
        });
    } else if (pathname === '/app/upload-test/result') {
      const testsDataLocal = JSON.parse(sessionStorage.getItem('testsData'));
      const urlParams = new URLSearchParams(window.location.search);
      const testId = urlParams.get('testId');
      getResultAPI(authToken, phone, testId)
        .then((response) => {
          this.setState({
            testId,
            result: response.data.result,
            testsData: testsDataLocal,
          });
        });
    }
  }

  componentDidUpdate(prevProps) {
    const { authToken, testsData, phone } = this.state;
    const { location: { pathname } } = this.props;
    const { location: { pathname: prevPathname } } = prevProps;
    if (pathname !== prevPathname) {
      const urlParams = new URLSearchParams(window.location.search);
      const testId = urlParams.get('testId');
      if (/upload-test\/?$/.test(pathname)) {
        getDashboardDataAPI(authToken, phone)
          .then((response) => {
            this.setState({
              testsData: response.data.data,
              cellData: [],
              result: '',
            });
          });
      } else if (/upload-test\/form/.test(pathname)) {
        const testData = testsData.filter((data) => (data.test_id === parseInt(testId, 10)))[0];
        getCellDataAPI(authToken, testData.batch)
          .then((response) => {
            this.setState({
              testId,
              cellData: response.data.cellData.map((label, index) => ({ label, isChecked: (testData.test_data === undefined || testData.test_data[index] === 100), value: testData.test_data ? testData.test_data[index].toString() : '100' })),
            }, this.checkCtaDisabled);
          });
      } else if (/upload-test\/result/.test(pathname)) {
        getResultAPI(authToken, phone, testId)
          .then((response) => {
            this.setState({
              testId,
              result: response.data.result,
            });
          });
      }
    }
  }

  handleChangeCellValue = (e) => {
    const { name, value, type } = e.target;
    let isCheckbox = false;
    if (type === 'checkbox') {
      isCheckbox = true;
    }
    if (isCheckbox || !value || (/^\d+(\.\d{0,5})?$/.test(value) && parseFloat(value) >= 0 && parseFloat(value) <= 50)) {
      const { cellData } = this.state;
      const cellDataNew = [...cellData];
      const cellIndex = cellData.findIndex((cell) => (cell.label === name));
      cellDataNew[cellIndex] = {
        label: name,
        isChecked: isCheckbox ? !cellData[cellIndex].isChecked : cellData[cellIndex].isChecked,
        value: isCheckbox ? (!cellData[cellIndex].isChecked ? '100' : '0') : value,
      };
      this.setState({
        cellData: cellDataNew,
      }, this.checkCtaDisabled);
    }
  }

  checkCtaDisabled = () => {
    const { location: { pathname } } = this.props;
    const { cellData } = this.state;
    let flag = true;
    if (/upload-test\/form/.test(pathname)) {
      const numValues = cellData.filter((cell) => (cell.value)).length;
      if (numValues === cellData.length) {
        flag = false;
      }
    } else {
      flag = true;
    }
    this.setState({
      isCtaDisabled: flag,
    });
  }

  submitCtValues = () => {
    const {
      testId, testsData, authToken, cellData,
      phone,
    } = this.state;
    const { history } = this.props;
    const testData = testsData.filter((data) => (data.test_id === parseInt(testId, 10)))[0];
    const { batch } = testData;
    uploadTestDataAPI(authToken, phone, testId,
      batch, cellData.map((cell) => (parseFloat(cell.value))))
      .then((response) => {
        console.log('data uploaded! ', response.data);
        if (response.status === 200) {
          history.replace(`/app/upload-test/result?testId=${testId}`);
        } else {
          console.log('Something went wrong: ', response.error);
        }
      });
  }

  render() {
    const {
      testsData,
      cellData,
      isCtaDisabled,
      result,
    } = this.state;
    const { location: { pathname } } = this.props;
    return (
      <div className="upload-test">
        <Switch>
          <Route exact path="/app/upload-test">
            <UploadTestLandingPage
              testsData={testsData}
            />
          </Route>
          <Route exact path="/app/upload-test/form">
            <UploadTestForm
              cellData={cellData}
              handleChangeCellValue={this.handleChangeCellValue}
            />
          </Route>
          <Route exact path="/app/upload-test/result">
            <UploadTestResult
              result={result}
              handleChangeCellValue={this.handleChangeCellValue}
            />
          </Route>
          <Route path="/app/upload-test/redirect">
            <div>Test Uploaded Successfully!</div>
          </Route>
        </Switch>
        {pathname === '/app/upload-test/form'
          ? (
            <div className="upload-test__cta">
              <button type="button" disabled={isCtaDisabled} onClick={this.submitCtValues}>Submit</button>
            </div>
          )
          : ''}
      </div>
    );
  }
}

UploadTest.propTypes = {
  location: PropTypes.shape({
    pathname: PropTypes.string.isRequired,
  }).isRequired,
  history: PropTypes.shape({
    push: PropTypes.func.isRequired,
    replace: PropTypes.func.isRequired,
  }).isRequired,
};

export default UploadTest;
