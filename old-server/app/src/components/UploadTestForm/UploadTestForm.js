import React, { useState } from 'react';
import PropTypes from 'prop-types';
import Select from 'react-select';
import './UploadTestForm.scss';

const CTInput = (props) => {
  const {
    cell,
    handleChangeCellValue,
  } = props;
  return (
    <div className="ct-input-box">
      <div className="ct-input-box-label">
        {cell.label}
      </div>
      <div className="ct-input-box-input">
        <div className="ct-input-box-input-checkbox">
          <input type="checkbox" name={cell.label} checked={cell.isChecked} onChange={handleChangeCellValue} />
          {' '}
          Threshold not reached
        </div>
        {cell.value !== '100' && (
        <div>
          <input type="tel" name={cell.label} value={cell.value} onChange={handleChangeCellValue} />
          {' Ct'}
        </div>
        )}
      </div>
    </div>
  );
};

CTInput.propTypes = {
  cell: PropTypes.shape({
    label: PropTypes.string,
    isChecked: PropTypes.bool,
    value: PropTypes.string,
  }),
  handleChangeCellValue: PropTypes.func.isRequired,
};

CTInput.defaultProps = {
  cell: {
    label: '',
    value: '',
  },
};

const UploadTestForm = (props) => {
  console.log('props: ', props);
  const {
    cellData, handleChangeCellValue, availableMatrices, selectedMatrix,
    handleMatrixChange, handleSampleSizeChange, selectedSampleSize,
  } = props;
  const options = availableMatrices.map((matrixObj) => {
    const value = Object.keys(matrixObj)[0];
    const label = `${value.split('_')[0]} ${matrixObj[value]}`;
    return {
      label,
      value,
    };
  });
  const [isUsingPdf, setIsUsingPdf] = useState(false);
  return (
    <div className="upload-test-form">
      <div className="upload-test-form-test-mode">
        <div className="upload-test-form-test-mode-title">Test Mode</div>
        <div className="upload-test-form-test-mode-radio-group">
          <div>
            <label htmlFor="appguide">
              <input type="radio" id="appguide" checked={!isUsingPdf} onClick={() => { setIsUsingPdf(false); }} />
              <b>Using app guide</b>
            </label>
          </div>
          <div>
            <label htmlFor="pdfprintout">
              <input type="radio" id="pdfprintout" checked={isUsingPdf} onClick={() => { setIsUsingPdf(true); }} />
              Offline Test with PDF printout
            </label>
          </div>
        </div>
        {isUsingPdf
          ? (
            <div className="upload-test-form__matrix-dropdown">
              <div className="upload-test-form__matrix-dropdown-label">Matrix Used</div>
              <div className="upload-test-form__matrix-dropdown-input">
                <Select
                  options={options}
                  value={selectedMatrix}
                  onChange={handleMatrixChange}
                  components={{
                    IndicatorSeparator: () => null,
                  }}
                  styles={{
                    dropdownIndicator: (provided) => ({
                      ...provided,
                      color: '#00cc92',
                    }),
                    control: (provided) => ({
                      ...provided,
                      boxShadow: 'none',
                      borderRadius: '10px',
                      border: '2px solid #eee',
                    }),
                    menu: (provided) => ({
                      ...provided,
                      marginTop: '0px',
                      left: '50%',
                      transform: 'translateX(-50%)',
                      width: '98%',
                      borderRadius: '10px',
                      borderTopLeftRadius: '5px',
                      borderTopRightRadius: '5px',
                    }),
                    option: (provided) => ({
                      ...provided,
                      backgroundColor: '#fff',
                      color: '#777',
                      borderRadius: '10px',
                    }),
                  }}
                />
              </div>
            </div>
          )
          : ''}
        <div className="upload-test-form__samples">
          <div className="upload-test-form__samples-label">No. of Samples</div>
          <div className="upload-test-form__samples-input">
            <input type="tel" value={selectedSampleSize} onChange={handleSampleSizeChange} />
          </div>
        </div>
      </div>
      <div className="upload-test-form__title">
        Input Cycle Time
      </div>
      {cellData.map((cell) => (
        <CTInput
          key={cell.label}
          cell={cell}
          handleChangeCellValue={handleChangeCellValue}
        />
      ))}
    </div>
  );
};

UploadTestForm.propTypes = {
  cellData: PropTypes.arrayOf(PropTypes.shape({})),
  availableMatrices: PropTypes.arrayOf(PropTypes.shape({})),
  selectedMatrix: PropTypes.shape({}),
  selectedSampleSize: PropTypes.string,
  handleChangeCellValue: PropTypes.func.isRequired,
  handleMatrixChange: PropTypes.func.isRequired,
  handleSampleSizeChange: PropTypes.func.isRequired,
};

UploadTestForm.defaultProps = {
  cellData: [],
  availableMatrices: [],
  selectedMatrix: {},
  selectedSampleSize: '',
};

export default UploadTestForm;
