import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Link } from 'react-router-dom';
import axios from 'axios';
import React, { useEffect, useState } from 'react';
import LogoImg from "../../Logo.png"

function Navbarboot() {
  const [accessToken, setAccessToken] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get('http://localhost:8000/login/refresh')
      .then(response => {
        setAccessToken(response.data.access_token);
      })
      .catch(error => {
        setAccessToken(null);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);
  
  if (loading) {
    return <div>Loading...</div>;
  }

  const goBack = (e) => {
    window.history.back()
  }
  const goFront = (e) =>{
    window.history.forward()
    
  }

  return (
    <Navbar collapseOnSelect expand="lg" className="bg-body-tertiary">
      <Container>
        <button
        onClick={goBack}>◀</button>
        <button
        onClick={goFront}>▶</button>
        <Navbar.Brand as={Link} to="/Main">
        <img src={LogoImg} style={{ width: 'auto', height: '40px',maxWidth:'100%', objectFit:'contain',paddingLeft:'10px'
        }}/>
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="responsive-navbar-nav" />
        <Navbar.Collapse id="responsive-navbar-nav">
            <Nav className="me-auto">
              <Nav.Link as={Link} to="/Boardlist">자유게시판</Nav.Link>
              <Nav.Link href="#pricing">교수님</Nav.Link>
              <NavDropdown title="더보기" id="collapsible-nav-dropdown">
                <NavDropdown.Item as={Link} to="/StudyBoardlist" >스터디게시판</NavDropdown.Item>
                <NavDropdown.Item href="#action/3.2">
                  족보게시판
                </NavDropdown.Item>
                <NavDropdown.Item href="#action/3.3">00게시판</NavDropdown.Item>
                <NavDropdown.Divider />
                <NavDropdown.Item href="#action/3.4">
                  우리의 여정
                </NavDropdown.Item>
              </NavDropdown>
            </Nav>
          <Nav>
            {accessToken !== undefined ? (
              <>
                <Nav.Link as={Link} to="/MyInfo">내 정보</Nav.Link>
              </>
            ) : (
              <Nav.Link as={Link} to="/Login" eventKey={2}>로그인</Nav.Link>
            )}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default Navbarboot;