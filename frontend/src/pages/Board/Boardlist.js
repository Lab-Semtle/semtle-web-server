import React, { useState, useEffect } from 'react';
import Navbarboot from '../../components/Header/Navbarboot';
import './CommonTable.css';
import axios from 'axios';
import { Link } from 'react-router-dom';
import './Board.css'; // 스타일을 위한 CSS 파일 임포트

const CommonTableRow = ({ children }) => {
  return (
    <tr className="common-table-row">
      {children}
    </tr>
  );
};

const CommonTableColumn = ({ children }) => {
  return (
    <td className="common-table-column">
      {children}
    </td>
  );
};

const CommonTable = (props) => {
  const { headersName, children } = props;

  return (
    <table className="common-table">
      <thead>
        <tr>
          {headersName.map((item, index) => (
            <td className="common-table-header-column" key={index}>{item}</td>
          ))}
        </tr>
      </thead>
      <tbody>
        {children}
      </tbody>
    </table>
  );
};

function App() {
  const [boardData, setBoardData] = useState([]);
  const [pageCount, setPageCount] = useState(0);
  const [currentPage, setCurrentPage] = useState(0);
  const itemsPerPage = 10;

  const fetchData = async (page) => {
    try {
      const response = await axios.get(`http://127.0.0.1:8000/api/v1/Free_Board/Get?page=${page}&size=${itemsPerPage}`);
      setBoardData(response.data.Board_info);
      setPageCount(Math.ceil(response.data.total / itemsPerPage));
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  useEffect(() => {
    fetchData(currentPage);
  }, [currentPage]);

  const handlePageClick = (page) => {
    setCurrentPage(page);
  };

  const handlePreviousClick = () => {
    if (currentPage > 0) {
      setCurrentPage((prevPage) => prevPage - 1);
    }
  };

  const handleNextClick = () => {
    if (currentPage < pageCount - 1) {
      setCurrentPage((prevPage) => prevPage + 1);
    }
  };

  const getDisplayedPages = () => {
    const startPage = Math.floor(currentPage / 10) * 10;
    return [...Array(10).keys()].map(i => startPage + i).filter(i => i < pageCount);
  };

  return (
    <>
      <Navbarboot />
      <CommonTable headersName={['글번호', '제목', '등록일', '조회수']}>
        {boardData.length > 0 ? boardData.map((item, index) => (
          <CommonTableRow key={index}>
            <CommonTableColumn>{item.Board_no}</CommonTableColumn>
            <CommonTableColumn><Link to={`/Boardview/${index}`}>{item.Title}</Link></CommonTableColumn>
            <CommonTableColumn>{item.Create_date}</CommonTableColumn>
            <CommonTableColumn>{item.Views}</CommonTableColumn>
          </CommonTableRow>
        )) : <tr><td colSpan="4">No data available</td></tr>}
      </CommonTable>
      <div className="pagination-container">
        <button onClick={handlePreviousClick} disabled={currentPage === 0}>Previous</button>
        {getDisplayedPages().map((page) => (
          <button key={page} onClick={() => handlePageClick(page)} disabled={page === currentPage} className={page === currentPage ? 'active' : ''}>
            {page + 1}
          </button>
        ))}
        <button onClick={handleNextClick} disabled={currentPage >= pageCount - 1}>Next</button>
      </div>
      <div className="create-button-container">
        <button><Link to="/Boardcreate">게시물 쓰기</Link></button>
      </div>
    </>
  );
}

export default App;
