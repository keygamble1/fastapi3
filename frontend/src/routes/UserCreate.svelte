<script>
  import { push } from 'svelte-spa-router';
  import Error from "../components/Error.svelte";
  import fastapi from "../lib/api";
    let username=''
    let password1=''
    let password2=''
    let email=''
    let error={detail:[]}
    function post_user(event){
        event.preventDefault()
        let url="/api/user/create"
        let params={
            username:username,
            password1:password1,
            password2:password2,
            email:email
        }
        fastapi('post',url,params,
            // 이미실행됨여기서
            (json)=>{
                // 그이후에 실행하는거 get일경우 업뎃
                // post일경우 다른경로로가기
                push('/user-login')
            },
            (json_error)=>{
                error=json_error
            }
        )
    }

</script>

<div
    class="container"
>   
    
    <h5 class="border-bottom pb-2">회원가입</h5>
    <Error error={error}/>
    <form  method="post">
        <div class="mb-3">
            <label for="username">사용자이름</label>
            <input type="text" bind:value={username} id="username" class="form-control">
            <!-- name이 bind:value임 -->
        </div>
        <div class="mb-3">
            <label for="password1">비밀번호</label>
            <input type="password" bind:value={password1} id="password1" class="form-control">
            <!-- name이 bind:value임 -->
        </div>
        <div class="mb-3">
            <label for="password2">비밀번호확인</label>
            <input type="password" bind:value={password2} id="password2" class="form-control">
            <!-- name이 bind:value임 -->
        </div>
        <div class="mb-3">
            <label for="email">사용자이름</label>
            <input type="text" bind:value={email} id="email" class="form-control">
            <!-- name이 bind:value임 -->
        </div>
        <button type="submit" class="btn btn-primary" on:click="{post_user}">생성하기</button>
    </form>
</div>
