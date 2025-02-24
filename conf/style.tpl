<style>

.resellerContainer--theme {
	--theme-background: #f4f4f4;
	--theme--titleColor: #000000;
	--theme-textColor: #000000;
}

.naglowek {
	font-size: 24px;
	text-align: center;
}

.kk_title {
	background:#f0f0f0;
	text-align:center;
	margin-left:auto;
	margin-right:auto;
	margin-bottom:20px;
	width:1042px;
	border-bottom:1px solid #E1E1E1;
	padding: 10px 0px 10px 0px
    font-size:24px;
}

.spec_container {
	width:1042px;
	margin-left:auto;
	margin-right:auto;
	padding:0px;
}

.spec_line {
	width:1042px;
	background-color:#fafafa;
	border-top: 1px solid #f0f0f0;
	vertical-align:middle;
}

.spec_line:nth-child(odd) {
   background-color: #fafafa;
}
.spec_line:nth-child(even) {
   background-color: #f4f4f4;
}


.spec_line:hover {
	background-color:#E3E3E3
}


.feature_spec {
	display:inline-block;
	background-color:inherit;
	vertical-align:top;
	text-transform:uppercase;
	width:470px;
	font-weight:700;
	text-align:right;
	padding:5px;
	vertical-align:middle;

}

.value_spec {
	display:inline-block;
	background-color:inherit;
	padding:5px;
	margin-left:4%;
	max-width:100%;
	vertical-align:middle;
}

.N
{
	display:none;
}

@media (max-width: 965px)
{
	.kk_title
	{
		width:100%;
	}
	.spec_container
	{
		border:0px solid;
		width:100%;
		margin:auto;
	}
	.spec_line
	{
		width:100%;
	}
	.feature_spec
	{
		display:block;
		margin-left:0px;
		padding:0px;
		text-align:center;
		width:100%;
	}
.value_spec
	{
		padding: 5px 0px 5px 0px;
		margin:0px;
		text-align:center;
		display:block;
		width:100%;
	}
}
</style>
