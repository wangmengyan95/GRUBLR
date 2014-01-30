$(document).ready(function(){
	setInterval(changeIndexFooterIconColor,100);
	// setInterval(checkNewGrumblr,5000);


	//ajax form with image
	var profileFormSubmitOptions={
		url: "/editProfileForm",
		type: "post",
		beforeSubmit:  showRequest,  // pre-submit callback 
        success: profileFormSubmitCallbackFuncion
	};

	$("#editProfileForm").submit(function(){
		$(this).ajaxSubmit(profileFormSubmitOptions);
		return false;
	})


	$(".ProfileContainer").find("#editProfileForm").css("display","none");
	$(".ProfileContainer").find("#showProfileForm").css("display","block");



	$("#changePasswordButton").click(function(){
		$.post("/changePassword/",$("#changePasswordForm").serialize(),function(json){
			showErrorMessage(json,'all',$("#changePasswordForm").find("input"));
			if($.isEmptyObject(json)){
				alert("You have successfully changed your password!!");
				window.location.href="/profile";
			}
		});		
	})


	$(".PostGrumblrCommentButton").click(function(){
		var singleGRUBLRContainer=$(this).parents(".SingleGRUBLRContainer");
		var grumblrId=singleGRUBLRContainer.find(".GrumblrId").html();
		var comment=singleGRUBLRContainer.find(".ReplyInput").val();
		// console.log(grumblrId);
		// console.log(comment);
		$.post("/home/postGrumblrComment/",{"comment":comment,"grumblrId":grumblrId},function(json){
			if($.isEmptyObject(json)){
				//refresh comment list
				refreshCommentList(singleGRUBLRContainer)
			}
			else{
				// show error message
				var errorText="";
				var errors=json;
				for(errorType in errors){
					errorText+=errors[errorType];
				}
				alert(errorText);
			}
		})
	})

	$(".MessageToolbarItemLeft").click(function(){
		if($(this).html()=="Expand"){
			var singleGRUBLRContainer=$(this).parents(".SingleGRUBLRContainer");
			var replayContainer=singleGRUBLRContainer.find(".GrumblrReplyContainer");
			replayContainer.show(750, function(){
				// singleGRUBLRContainer.css("margin-top","10px");
				// singleGRUBLRContainer.css("margin-bottom","10px");
				// singleGRUBLRContainer.css("-webkit-box-shadow","0px 0px 5px #000000");
				// singleGRUBLRContainer.css("box-shadow","0px 0px 5px #000000");
				// singleGRUBLRContainer.find(".GrumblrMessageContainer").css("-webkit-box-shadow","0px 0px 5px #000000");
				// singleGRUBLRContainer.find(".GrumblrMessageContainer").css("box-shadow","0px 0px 5px #000000");
				singleGRUBLRContainer.animate({marginTop:"20px",marginBottom:"20px"},500);
				singleGRUBLRContainer.find(".GrumblrMessageContainer").animate({borderBottomStyle:"solid"},500);
			});

			//refresh comment list
			refreshCommentList($(this).parents(".SingleGRUBLRContainer"));

			//change link word
			$(this).html("Collapse")

		}else{
			var singleGRUBLRContainer=$(this).parents(".SingleGRUBLRContainer");
			var replayContainer=singleGRUBLRContainer.find(".GrumblrReplyContainer");
			replayContainer.hide(750,function(){
				// singleGRUBLRContainer.css("margin-top","0px");
				// singleGRUBLRContainer.css("margin-bottom","0px");
				// singleGRUBLRContainer.css("-webkit-box-shadow","0px 0px 0px #000000");
				// singleGRUBLRContainer.css("box-shadow","0px 0px 0px #000000");
				// singleGRUBLRContainer.find(".GrumblrMessageContainer").css("-webkit-box-shadow","0px 0px 0px #000000");
				// singleGRUBLRContainer.find(".GrumblrMessageContainer").css("box-shadow","0px 0px 0px #000000");
				singleGRUBLRContainer.animate({marginTop:"0px",marginBottom:"0px"},500);
				singleGRUBLRContainer.find(".GrumblrMessageContainer").animate({borderBottomStyle:"none"},500)
			});
			$(this).html("Expand");
		}
	})

	// $("#postGrumblrButton").click(function(){
	// 	// console.log($("textarea").val());
	// 	$.post("/home",{"content":$("textarea").val()},function(json){
	// 		window.location.href = './home';
	// 	})
	// })

	// var imageState="small";
	// var imageHeight=0;
	// var imageWidth=0;
	$(".GrumblrImage").click(function(){
		if($(this).data("size")=="small"){
			$(this).data("formerHeight",$(this).css("height"));
			$(this).data("formerWidth",$(this).css("width"));
			$(this).data("size","large");
			$(this).css({height:"100%",width:"100%"})
			changeGrumblrContainerHeight();
		}
		else{
			var formerHeight=$(this).data("formerHeight");
			var formerWidth=$(this).data("formerWidth");
			$(this).data("size","small");
			$(this).css({height:formerHeight,width:formerWidth});
			changeGrumblrContainerHeight();
		}

	})


	$("#postGrumblrForm").submit(function(){
		if(!$(this).find("textarea").val()){
			alert("Please type something :-)");
			event.preventDefault();
		}
	})

	$(".LogOutIcon").click(function(){
		window.location.href = "/logout";
	})
	$("#birthdayPicker").datepicker({ dateFormat: "yy-mm-dd" });

	$(".NeedCheckInputField").blur(function(){
		var inputField=$(this);
		name=inputField.attr("name");
		value=inputField.val();
		var form={
			name: value,
		};

		// console.log($("#registerInfoForm").serialize());

		$.post("/checkRegisterForm",$("#registerInfoForm").serialize(),function(json){
			showErrorMessage(json,'single',inputField);
		});
	})
	$("#signInButton").click(function(){
		// console.log(1);
		// console.log($("#logInForm"));
		$.post("/login", $("#logInForm").serialize(),function(data){
			// console.log(data);
		});
	})
	$("#registerStartButton").click(function(){
		$("#logInForm").hide(1000, function(){
			$("#registerForm").show(1000);
		});
	});

	$("#registerFinishButton").click(function(){
		// $("#registerInfoForm").valid();
		// console.log(1);
		$.post("/register", $("#registerInfoForm").serialize(), function(json){
			// console.log(json);
			if($.isEmptyObject(json)){
				var name=$("#userName").val();

				$("#registerForm").hide(100,function(){
					$("#welcomeForm").show(100,function(){
						var delay=showWelcomeLogo(name);
						setTimeout(function(){
							window.location.href = "/home";
						},(delay+20)*100)
					})
				})
			}
			else{
				showErrorMessage(json,'all',$("#registerInfoForm").find(".NeedCheckInputField"));
			}
		})
	});

	// $(".RefreshBar").click(function(){
	// 	 var latestGrumblrTime=$(".GrumblrPublishTime").html();
	// 	 console.log(latestGrumblrTime);
	// 	 $.post("/refreshGrumblrList/",{"latestGrumblrTime":latestGrumblrTime},function(json){
	// 	 	console.log(json);

	// 		var templateSingleGRUBLRContainer = $(".SingleGRUBLRContainer:last").clone(true,true);
	// 		$(".SingleGRUBLRContainer").remove();
	// 	 	for(var i=json.grumblrList.length-1;i>=0;i--){
	// 	 		grumblr=json.grumblrList[i];
	// 		 	var newSingleGRUBLRContainer = templateSingleGRUBLRContainer.clone(true,true);
	// 	 		newSingleGRUBLRContainer.find('.MessageTitle a').html(grumblr.owner);
	// 	 		newSingleGRUBLRContainer.find('.MessageText').html(grumblr.content);
	// 	 		newSingleGRUBLRContainer.find('.GrumblrId').html(grumblr.id);
	// 	 		newSingleGRUBLRContainer.find('.GrumblrPublishTime').html(grumblr.publishDateTime);
	// 	 		newSingleGRUBLRContainer.find('.ThumbUpButton').html("<i class=\"icon-thumbs-up\"></i>"+"("+grumblr.thumbUp+")")

	// 	 		newSingleGRUBLRContainer.find('img').attr("src","/getAvatar/"+grumblr.owner);
	// 	 		newSingleGRUBLRContainer.insertAfter($(".RefreshBarContainer"));	 	
	// 	 	}

	// 	 	// for (grumblr in json.grumblrList){
	// 		 // 	var newSingleGRUBLRContainer = $(".SingleGRUBLRContainer:last").clone(true,true);
	// 	 	// 	newSingleGRUBLRContainer.find('.MessageTitle a').html(grumblr.owner);
	// 	 	// 	console.log(json.grumblrList[0]);
	// 	 	// 	console.log("/getAvatar/"+grumblr.owner);
	// 	 	// 	newSingleGRUBLRContainer.find('img').attr("src","/getAvatar/"+grumblr.owner);
	// 	 	// 	newSingleGRUBLRContainer.insertAfter($(".RefreshBarContainer"));
	// 	 	// }
	// 	 })
	// });

	// $(".GrumblrMessageContainer").css("height",function(index,value){

	// 	var messageContainer=$(this).find($(".MessageContainer"));
	// 	var messageToolbar=$(this).find($(".MessageToolbar"));

	// 	// var grumblrMessageContainer=$(this).parent(".GrumblrMessageContainer");
	// 	// var avatarContainer=$(this).
	// 	// console.log(messageContainer.height());
	// 	// console.log(messageToolbar.height());

	// 	return messageToolbar.height()+messageContainer.height()+10;
	// });
	$(".GrumblrMessageContainer .GRUBLRMessage").css("height",function(){
		// var headImageHeight=$(this).parent().height();
		// var currentHeight=$(this).height();
		// if(currentHeight<headImageHeight) return headImageHeight;
		// else return currentHeight;

		// console.log($(this).parent());
		// console.log($(this).parent().height());
		var messageContainerHeight=$(this).find(".MessageContainer").height();
		var messageToolbarHeight=$(this).find(".MessageToolbar").height();
		// return $(this).parent().height();
		return messageContainerHeight+messageToolbarHeight+10;
	})

	$("#ProfileEditBasicButton").click(function(){
		var button=$(this);
		var editContainer=$(".ProfileEditBasicContainer .ProfileContainer");
		if($(this).html()=="Edit"){		

			//show input 
			editContainer.hide(1000,function(){
				button.html("Save");
				editContainer.find("#showProfileForm").css("display","none");
				editContainer.find("#changePasswordForm").css("display","none");
				editContainer.find("#editProfileForm").css("display","block");
				editContainer.show(1000);

			});
		}
		else{	
			$("#editProfileForm").trigger("submit");
		}
	});
});

base=0.6;
deltaBase=0.1;
function changeIndexFooterIconColor(){
	if($(".IndexFooterIcon")){
		// color=256-Math.round(256*base);
		opacity=base;
		// $(".logInFooterIcon").animate({borderColor: "rgb("+color+","+color+","+color+")"},100);
		$(".IndexFooterIcon").animate({opacity: opacity},100);
		if(base>=0.6) deltaBase=-0.02;
		if(base<=0) deltaBase=0.01;
		base=base+deltaBase;
		// console.log(color+" "+opacity);
	}
}


$(document).ajaxSend(function(event, xhr, settings) {  
    function getCookie(name) {  
        var cookieValue = null;  
        if (document.cookie && document.cookie != '') {  
            var cookies = document.cookie.split(';');  
            for (var i = 0; i < cookies.length; i++) {  
                var cookie = jQuery.trim(cookies[i]);  
                // Does this cookie string begin with the name we want?  
                if (cookie.substring(0, name.length + 1) == (name + '=')) {  
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));  
                    break;  
                }  
            }  
        }  
        return cookieValue;  
    }  
    function sameOrigin(url) {  
        // url could be relative or scheme relative or absolute  
        var host = document.location.host; // host + port  
        var protocol = document.location.protocol;  
        var sr_origin = '//' + host;  
        var origin = protocol + sr_origin;  
        // Allow absolute or scheme relative URLs to same origin  
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||  
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||  
            // or any other URL that isn't scheme relative or absolute i.e relative.  
            !(/^(\/\/|http:|https:).*/.test(url));  
    }  
    function safeMethod(method) {  
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));  
    }  
  
    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {  
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));  
    }  
}); 


// 

function checkNewGrumblr(){
	// $(".RefreshBar").css("display","block");
	var $RefreshBar = $(".RefreshBar");
	$RefreshBar.html("<i class=\"icon-refresh icon-spin\"></i>Refreshing");
	$RefreshBar.slideDown(300);



	 var latestGrumblrTime=$(".GrumblrPublishTime").html();
	 console.log(latestGrumblrTime);
	 $.post("/refreshGrumblrList/",{"latestGrumblrTime":latestGrumblrTime},function(json){
	 	console.log(json);

		var templateSingleGRUBLRContainer = $(".SingleGRUBLRContainer:last").clone(true,true);
		$(".SingleGRUBLRContainer").remove();
	 	for(var i=json.grumblrList.length-1;i>=0;i--){
	 		grumblr=json.grumblrList[i];
		 	var newSingleGRUBLRContainer = templateSingleGRUBLRContainer.clone(true,true);
	 		newSingleGRUBLRContainer.find('.MessageTitle a').html(grumblr.owner);
	 		newSingleGRUBLRContainer.find('.MessageText').html(grumblr.content);
	 		newSingleGRUBLRContainer.find('.GrumblrId').html(grumblr.id);
	 		newSingleGRUBLRContainer.find('.GrumblrPublishTime').html(grumblr.publishDateTime);
	 		newSingleGRUBLRContainer.find('.ThumbUpButton').html("<i class=\"icon-thumbs-up\"></i>"+"("+grumblr.thumbUp+")")

	 		newSingleGRUBLRContainer.find('.AvatarImage').attr("src","/getAvatar/"+grumblr.owner);
			if(grumblr.image!="")newSingleGRUBLRContainer.find('.GrumblrImage').attr("src","/getGrumblrImage/"+grumblr.image).css("display","block");
			else newSingleGRUBLRContainer.find('.GrumblrImage').attr("src","").css("display","none");
	 		newSingleGRUBLRContainer.insertAfter($(".RefreshBarContainer"));	 	
	 	}

		$(".GrumblrMessageContainer .GRUBLRMessage").css("height",function(){
			var messageContainerHeight=$(this).find(".MessageContainer").height();
			var messageToolbarHeight=$(this).find(".MessageToolbar").height();
			// return $(this).parent().height();
			return messageContainerHeight+messageToolbarHeight+10;
		})

	 	$RefreshBar.delay(800).slideUp(300);//Refreshbar hide
	 })


}


function showErrorMessage(errors,type,field){

	if(type=='single'){	
		var inputField=field;

		name=inputField.attr("name");

		var icons=inputField.parent().find("i");

		var hasError=false;

		//delete former error messag
		inputField.parent().find("label").remove();

		for(var errorType in errors){
			if(errorType.toLowerCase()==name.toLowerCase()){

				icons.fadeOut(500);
				$(icons[1]).fadeIn(500);					
				inputField.parent().append("<label class=\"error\">"+errors[errorType]+"</label>")
				hasError=true
			}
		}
		if(!hasError){
			icons.fadeOut(500);
			$(icons[0]).fadeIn(500);			
		}

	}
	else if(type=='all'){
		for(var i=0;i<=field.length-1;i++){
			var inputField=$(field[i]);

			//delete former error message
			inputField.parent().find("label").remove();

			name=inputField.attr("name");

			var icons=inputField.parent().find("i");

			var hasError=false;


			for(var errorType in errors){
				if(errorType.toLowerCase()==name.toLowerCase()){

					icons.fadeOut(500);
					$(icons[1]).fadeIn(500);					
					inputField.parent().append("<label class=\"error\">"+errors[errorType]+"</label>")
					hasError=true
				}
			}
			if(!hasError){
				icons.fadeOut(500);
				$(icons[0]).fadeIn(500);			
			}
		}
	}
}



function showWelcomeLogo(userName){
	var text="Browser:~"+userName+"$ Hello "+userName+"!";
	text+="Browser:~"+userName+"$ sudo .\\GRUBLR";
	var logo=$("#welcomeLogo");
	logo.text(text);
	logo.ghostType();
	return text.length;
}
function refreshCommentList(SingleGRUBLRContainer){
	var grumblrId=SingleGRUBLRContainer.find(".GrumblrId").html();

	var grumblrReplyContainer=SingleGRUBLRContainer.find(".GrumblrReplyContainer");
	var replyInputContainer=grumblrReplyContainer.find(".ReplyInputContainer");
	var replyMessageContainer=grumblrReplyContainer.find(".ReplyMessageSampleContainer");

	console.log(replyInputContainer);
	console.log(replyMessageContainer);

	$.post('/home/getGrumblrComment/',{'grumblrId':grumblrId},function(json){
		console.log(json);
		$(".ReplyMessageContainer").remove();
		// grumblrReplyContainer.remove(".ReplyMessageContainer");
		// grumblrReplyContainer.append("<div class=\"ReplyInputContainer\">"+replyInputContainer.html()+"</div>");
		//add comment
		for(var i=0;i<=json.authorList.length-1;i++){
			var newReplyMessageContainer=replyMessageContainer.clone(true,true);
			newReplyMessageContainer.find(".ReplyUser").html(json.authorList[i]);
			newReplyMessageContainer.find(".ReplyContent").html(json.contentList[i]);
			//comment user avatar
			newReplyMessageContainer.find(".CommentUserAvatar").attr("src","/getAvatar/"+json.authorList[i]);
			grumblrReplyContainer.append("<div class=\"ReplyMessageContainer\">"+newReplyMessageContainer.html()+"</div>");
		}



	})
}





// pre-submit callback 
function showRequest(formData, jqForm, options) { 
    // formData is an array; here we use $.param to convert it to a string to display it 
    // but the form plugin does this for you automatically when it submits the data 
    // var queryString = $.param(formData); 
 
    // jqForm is a jQuery object encapsulating the form element.  To access the 
    // DOM element for the form do this: 
    // var formElement = jqForm[0]; 
 
    // alert('About to submit: \n\n' + queryString); 
 
    // here we could return false to prevent the form from being submitted; 
    // returning anything other than false will allow the form submit to continue 
    return true; 
} 

// post-submit callback 
function profileFormSubmitCallbackFuncion(json, statusText, xhr, $form)  { 

    // alert('status: ' + statusText + '\n\nresponseText: \n' + json + 
    //     '\n\nThe output div should have already been updated with the responseText.'); 

    console.log(json);

	var editContainer=$(".ProfileEditBasicContainer .ProfileContainer");
	if($.isEmptyObject(json)){
		//no error

		//ask new profile
		$.post("/getProfile",{},function(json){
			console.log(json);
			if(json.getProfileSuccess==true){

				//progress bar
				// var percentVal = '100%';
				// $('.bar').width(percentVal)
				// $('.percent').html(percentVal);

				//change label
				editContainer.find("#profileEmail").html(json.email);
				editContainer.find("#profileFirstName").html(json.firstName);
				editContainer.find("#profileLastName").html(json.lastName);
				editContainer.find("#profileBirthday").html(json.birthday);
				var $selfImg= $(".AvatarImage img");
			  	$selfImg.attr('src', $selfImg.attr('src') + '?' + Math.random());


				//label show input off
				editContainer.hide(1000,function(){
					$("#ProfileEditBasicButton").html("Edit");
					editContainer.find("#editProfileForm").css("display","none");
					editContainer.find("#showProfileForm").css("display","block");
					editContainer.show(1000);
				});			
			}
		});	
	}
	else{
		// console.log(2);
		showErrorMessage(json,'all',$("#editProfileForm").find("input"));

		//progress bar
		// var percentVal = '100%';
		// console.log($('.bar'));
		// $('.bar').width(percentVal)
		// $('.percent').html(percentVal);
	}	
} 
function changeGrumblrContainerHeight(){
	$(".GrumblrMessageContainer .GRUBLRMessage").css("height",function(){
	var messageContainerHeight=$(this).find(".MessageContainer").height();
	var messageToolbarHeight=$(this).find(".MessageToolbar").height();
	return messageContainerHeight+messageToolbarHeight+10;
})
}