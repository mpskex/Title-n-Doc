/*
#	mpsk
#	Beijing University of Technology
#	Copyright 2018
*/
function postdata() 
{
    document.getElementById("sform").submit()
}

function genExp()
{
    var dist = document.getElementById('dist').innerHTML;
    var _str = "";
    dist = parseFloat(dist);
    if(dist >=0 && dist <0.1)
    {
        _str = "几乎是完全吻合<br>你是不是复制粘贴来着:/";
    }
    else if(dist >=0.1 && dist <0.2)
    {
        _str = "感觉说的还是挺搭边儿的～";
    }
    else if(dist >=0.2 && dist <0.4)
    {
        _str = "其实我觉得吧<br>这不能说是题文对应";
    }
    else if(dist >=0.4 && dist <0.6)
    {
        _str = "完全说的不是一件事";
    }
    else if(dist >=0.6 && dist < 1)
    {
        _str = "(死鱼眼)buzai guna!"
    }
    else
    {
        _str = "Are you speaking Chinese???("
    }

    document.getElementById('explain').innerHTML = _str;
}