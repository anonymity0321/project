document.getElementById('loginForm').addEventListener('submit', function(event) {
  event.preventDefault(); // 阻止表单默认提交行为

  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  if (username && password) {
    alert(`登录成功！\n用户名: ${username}`);
    // 这里可以添加实际的登录逻辑，例如发送请求到后端验证用户信息
  } else {
    alert('请填写用户名和密码！');
  }
});