import { Injectable } from '@angular/core';

@Injectable()
export class UserAndTokenService {
    private userAndToken: Object;
    getUserAndToken(){
        return {token: this.userAndToken}
    }
    setUserAndToken(userAndToken){
        this.userAndToken = userAndToken;
    }
}