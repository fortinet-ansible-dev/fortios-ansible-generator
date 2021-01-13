  function ContentClick(elementid, btnid) {

      // display the content
      if (document.getElementById(elementid).clicked == undefined ||
          document.getElementById(elementid).clicked == false) {
          document.getElementById(elementid).clicked = true;
          document.getElementById(elementid).style.display = '';
          document.getElementById(btnid).text = 'less...';
      } else {
          document.getElementById(elementid).style.display = 'none';
          document.getElementById(elementid).clicked = false;
          document.getElementById(btnid).text = 'more...';
      }
  }

  function ContentPreview(elementid) {
      if (document.getElementById(elementid).clicked == false ||
          document.getElementById(elementid).clicked == undefined) {
          document.getElementById(elementid).style.display = '';
      }
      document.getElementById(elementid).underpreview = true;
  }

  function ContentUnpreview(elementid) {
    if (document.getElementById(elementid).clicked == false ||
        document.getElementById(elementid).clicked == undefined) {
        document.getElementById(elementid).style.display = 'none';
    }
    document.getElementById(elementid).underpreview = false;
  }
