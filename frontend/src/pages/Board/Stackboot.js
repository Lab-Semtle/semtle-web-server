import React, { useState, useEffect } from 'react';
import Navbarboot from '../../components/Header/Navbarboot';
import './CommonTable.css';
import axios from 'axios';

const CommonTableRow = ({ children }) => {
  return (
    <tr className="common-table-row">
      {
        children
      }
    </tr>
  )
}
const CommonTableColumn = ({ children }) => {
  return (
    <td className="common-table-column">
      {
        children
      }
    </td>
  )
}
const CommonTable = (props) => {
  const { headersName, children } = props;

  return (
      <table className="common-table">
        <thead>
          <tr>
            {
              headersName.map((item, index) => {
                return (
                  <td className="common-table-header-column" key={index}>{ item }</td>
                )
              })
            }
          </tr>
        </thead>
        <tbody>
          {
            children
          }
        </tbody>
      </table>
    )
}

function App() {
  const [BoardData, setBoardData] = useState([]); // 상태와 상태 업데이트 함수 이름 변경

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/v1/Free_Board/Get');
        setBoardData(response.data); // 받아온 데이터로 상태 업데이트
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
    fetchData();
  }, []);

  return (
    <>
      <Navbarboot />
      <CommonTable headersName={['글번호', '제목', '등록일', '조회수']}>
        {
          BoardData.length > 0 ? BoardData.map((item, index) => (
            <CommonTableRow key={index}>
              <CommonTableColumn>{item.Board_no}</CommonTableColumn>
              <CommonTableColumn>{item.Title}</CommonTableColumn>
              <CommonTableColumn>{item.Create_date}</CommonTableColumn>
              <CommonTableColumn>{item.Views}</CommonTableColumn>
            </CommonTableRow>
          )) : <tr><td colSpan="4">No data available</td></tr>
        }
      </CommonTable>
    </>
  );
}

export default App;