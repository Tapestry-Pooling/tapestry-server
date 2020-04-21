import React from 'react';
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
  const { cellData, handleChangeCellValue } = props;
  const options = [
    { value: 'chocolate', label: 'Chocolate' },
    { value: 'strawberry', label: 'Strawberry' },
    { value: 'vanilla', label: 'Vanilla' },
  ];
  return (
    <div className="upload-test-form">
      <div className="upload-test-form__matrix-dropdown">
        <div className="upload-test-form__matrix-dropdown-label">Select Matrix</div>
        <div className="upload-test-form__matrix-dropdown-select">
          <Select
            options={options}
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
                borderColor: '#ccc',
              }),
            }}
          />
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
  handleChangeCellValue: PropTypes.func.isRequired,
};

UploadTestForm.defaultProps = {
  cellData: [],
};

export default UploadTestForm;
